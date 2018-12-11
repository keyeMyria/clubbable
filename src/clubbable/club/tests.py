from datetime import date
from django.conf import settings
from django.test import TestCase
from club.models import Member, Guest, Meeting


class TestMember(TestCase):

    def setUp(self):
        self.orig_member_title = settings.MEMBER_TITLE
        self.member = Member(
            title='Sir',
            initials='M.E.',
            last_name='Palin',
            post_title='CBE FRGS',
            familiar_name='Michael'
        )

    def tearDown(self):
        settings.MEMBER_TITLE = self.orig_member_title

    def test_unicode_with_member_title(self):
        settings.MEMBER_TITLE = 'Rotarian'
        self.assertEqual('%s' % self.member, 'Rotarian Michael Palin')

    def test_unicode_without_member_title(self):
        settings.MEMBER_TITLE = None
        self.assertEqual('%s' % self.member, 'Michael Palin')

    def test_get_formal_name(self):
        self.assertEqual(self.member.get_formal_name(),
                         'Sir M.E. Palin CBE FRGS')

    # TODO: Test sync_email
    # def test_sync_email(self):
    #     ...


class TestGuest(TestCase):

    def test_unicode(self):
        guest = Guest(
            title='Mr',
            first_name='Eric',
            last_name='Idle'
        )
        self.assertEqual('%s' % guest, 'Mr Eric Idle')


class TestMeeting(TestCase):

    def test_unicode(self):
        meeting = Meeting(
            year=2013,
            month=2,
            date=date(2014, 3, 22),
            name='Meeting'
        )
        self.assertEqual('%s' % meeting, 'Meeting (March 2014)')
