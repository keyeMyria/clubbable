"""
Member, Guest and Event classes form the core of *clubbable*.

The class definitions include a field name in comments after each field. This
corresponds the the field in the Microsoft Access database that is imported to
populate *clubbable*.

The import tool is src/clubbable/dbtools/importmdb.py. It is specific to the
club for which *clubbable* is written, but should be easy to customise for
other clubs, or simply ignored if the club does not use a Microsoft Access
database.

"""
from __future__ import unicode_literals
from django.conf import settings
from django.core.mail import mail_admins
from django.db import models
from django.db.models.signals import post_save


class Member(models.Model):
    """
    Member instances can be sent e-mails. They and Guest instances are
    associated with gallery images.
    """
    id = models.PositiveIntegerField(primary_key=True)  # OwlID
    title = models.CharField(max_length=100, blank=True)  # Title
    initials = models.CharField(max_length=100)  # Initials
    last_name = models.CharField(max_length=100)  # Lastname
    post_title = models.CharField(max_length=100, blank=True)  # PostTitle
    familiar_name = models.CharField(max_length=100)  # FamiliarName
    # Address Label Sheet
    # Address1
    # Address2
    # Address3
    # Address4
    # Address5
    # Address6
    year = models.PositiveIntegerField(null=True, blank=True)  # Year
    # MembershipCategory
    # Interests -- Not authoritative. Use booleans below instead.
    # PastPresident
    # RegularDiner
    # CaptureDateOfLastChange
    # EffectiveDateOfLastChange
    # Comment
    # Birthdate
    # HomeTelephone
    # WorkTelephone
    # MobileTelephone
    email = models.CharField(max_length=150, blank=True)  # EmailAddress
    send_emails = models.BooleanField(default=False)  # ReceivesNoticesElectronically
    # Proposer
    # Seconder
    # SpouseName
    # PreferredFax
    # AddressCategory
    qualification_art = models.BooleanField(default=False)  # Art
    qualification_drama = models.BooleanField(default=False)  # Drama
    qualification_literature = models.BooleanField(default=False)  # Literature
    qualification_music = models.BooleanField(default=False)  # Music
    qualification_science = models.BooleanField(default=False)  # Science
    hon_life_member = models.BooleanField(
        verbose_name='Honorary life member',
        default=False)  # HonLifeMember
    canonisation_date = models.DateField(null=True,
                                         blank=True)  # CanonisationDate
    # Category
    # ExternalRole1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('last_name', 'familiar_name')

    def __str__(self):
        return self.get_full_name()

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        if settings.MEMBER_TITLE:
            return ' '.join([settings.MEMBER_TITLE,
                             self.familiar_name,
                             self.last_name])
        return ' '.join([self.familiar_name, self.last_name])

    def get_formal_name(self):
        return ' '.join([
            self.title,
            self.initials,
            self.last_name,
            self.post_title,
        ])

    @staticmethod
    def sync_email(sender, instance, created, raw, using, update_fields,
                   **kwargs):
        """
        Compare e-mail address with that of corresponding user (if exists). If
        necessary, sync and notify admin.
        """
        member = instance
        if not member.profile_set().count():
            # This member does not have an associated user
            return
        user = member.profile_set().get().user
        if user.email == member.email:
            # The e-mail address did not change
            return
        message = 'The e-mail address of {} has changed from {} to {}.'.format(
            member, user.email, member.email)
        user.email = member.email
        user.save()
        mail_admins('User address changed', message)


post_save.connect(Member.sync_email, sender=Member)


class Guest(models.Model):
    """
    Guest and Member instances are associated with gallery images.
    """
    id = models.PositiveIntegerField(primary_key=True,
                                     editable=False)  # GuestID Int8,
    date_of_listing = models.DateField()  # DateOfListing Timestamp,
    last_name = models.CharField(max_length=100)  # GuestLastName Char (100),
    first_name = models.CharField(max_length=100)  # GuestFirstName Char (100),
    initials = models.CharField(max_length=100)  # GuestInitials Char (100),
    title = models.CharField(max_length=100)  # GuestTitle Char (100),
    admitted_to_club = models.BooleanField(default=False)  # AdmittedToOwldom Bool,
    date_admitted = models.DateField(null=True,
                                     blank=True)  # DateAdmitted Timestamp,
    member = models.ForeignKey(Member, null=True, blank=True)  # MemberNum Int8,
    delisted = models.BooleanField(default=False)  # Delisted Bool
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        return ' '.join([self.title, self.first_name, self.last_name])

    def __unicode__(self):
        return ' '.join([self.title, self.first_name, self.last_name])


class Meeting(models.Model):
    """
    Gallery images may be associated with an Meeting.
    """
    id = models.PositiveIntegerField(primary_key=True,
                                     editable=False)  # EventNum Int8,
    year = models.PositiveIntegerField()  # Year Int8,
    month = models.PositiveIntegerField()  # Month Int8,
    date = models.DateField()  # EventDate Timestamp,
    name = models.CharField(max_length=100, blank=True)  # Name Char (100),
    status = models.CharField(max_length=100, blank=True)  # Status Char (100),
    number_of_tables = models.PositiveSmallIntegerField()  # NumberOfTables Int4
    comment = models.CharField(max_length=100, blank=True)  # Comment Char (100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Note that the year and month fields are ignored. Just the date field
        # is used. This is because we import the year and month fields, if they
        # are available, for the sake of completeness
        return '{} ({})'.format(self.name, self.date.strftime('%B %Y'))

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.date.strftime('%B %Y'))
