"""
Import Owls, guests and events from Owldom Access database.
"""

import csv
from datetime import datetime
import re
from subprocess import Popen, PIPE
from celery import shared_task
from django.conf import settings
from club.models import Member, Meeting, Guest


def to_iso_date(matches):
    """Converts regex match object into YYYY-MM-DD string
    """
    mm, dd, yy = matches.groups()
    now = datetime.now()
    if int(yy) > (now.year % 100):
        # Must be last century
        last_c = now.year // 100 - 1
        yyyy = str(last_c) + yy
    else:
        yyyy = str(now.year // 100) + yy
    return '%s-%s-%s' % (yyyy, mm, dd)


class MdbImporter(object):

    def __init__(self, mdb_file):
        self.mdb_file = mdb_file
        self.date_pattern = (r'^(\d{2})/(\d{2})/(\d{2}) 00:00:00', to_iso_date)

    def _import_table(self, class_, table, id, attributes):
        """Imports a table from an Access database.

        @param class_: The Django ORM to populate
        @param table: The Access database table name
        @param id: The name of the primary key field
        @param attributes: A tuple of attribute-column tuples
        """
        # Mark the start time
        start = datetime.now()
        # Run the mdb-export command
        args = (settings.MDB_EXPORT_CMD, self.mdb_file, table)
        p = Popen(args, stdout=PIPE)
        # Read output as CSV
        reader = csv.DictReader(p.stdout)
        lines = 0
        for row in reader:
            lines += 1
            try:
                obj = class_.objects.get(pk=row[id])
            except class_.DoesNotExist:
                obj = class_(id=row[id])
            for attr, column, nullable, pattern in attributes:
                if nullable and len(row[column]) == 0:
                    value = None
                elif pattern is not None:
                    value = re.sub(pattern[0], pattern[1], row[column])
                else:
                    value = row[column]
                setattr(obj, attr, value)
            obj.save()
        # Validate update succeeded
        if 1 < lines == class_.objects.filter(updated_at__gte=start).count():
            # Delete all events not found in import
            class_.objects.filter(updated_at__lt=start).delete()

    def import_members(self):
        """Import from the OwlsPersonalDetails table
        """
        attributes = (
            # ORM attribute, Owldom field, Is nullable, Transformation pattern
            ('title', 'Title', False, None),
            ('initials', 'Initials', False, None),
            ('last_name', 'Lastname', False, None),
            ('post_title', 'PostTitle', False, None),
            ('familiar_name', 'FamiliarName', False, None),
            ('year', 'Year', True, None),
            ('email', 'EmailAddress', False, None),
            ('send_emails', 'ReceivesNoticesElectronically', False, None),
            ('qualification_art', 'Art', False, None),
            ('qualification_drama', 'Drama', False, None),
            ('qualification_literature', 'Literature', False, None),
            ('qualification_music', 'Music', False, None),
            ('qualification_science', 'Science', False, None),
            ('hon_life_member', 'HonLifeMember', False, None),
            ('canonisation_date', 'CanonisationDate', True, self.date_pattern),
        )
        self._import_table(Member, 'OwlsPersonalDetails', 'OwlID', attributes)

    def import_guests(self):
        attributes = (
            ('date_of_listing', 'DateOfListing', True, self.date_pattern),
            ('last_name', 'GuestLastName', False, None),
            ('first_name', 'GuestFirstName', False, None),
            ('initials', 'GuestInitials', False, None),
            ('title', 'GuestTitle', False, None),
            ('admitted_to_owldom', 'AdmittedToOwldom', False, None),
            ('date_admitted', 'DateAdmitted', True, self.date_pattern),
            ('owl_id', 'MemberNum', True, None), # TODO: Test
            ('delisted', 'Delisted', False, None),
        )
        self._import_table(Guest, 'Guests', 'GuestID', attributes)

    def import_meetings(self):
        attributes = (
            ('year', 'Year', False, None),
            ('month', 'Month', False, None),
            ('date', 'EventDate', False, self.date_pattern),
            ('name', 'Name', False, None),
            ('status', 'Status', False, None),
            ('number_of_tables', 'NumberOfTables', False, None),
            ('comment', 'Comment', False, None),
        )
        self._import_table(Meeting, 'Events', 'EventNum', attributes)


@shared_task
def import_mdb(filename):
    importer = MdbImporter(filename)
    importer.import_members()
    importer.import_guests()
    importer.import_meetings()
