from __future__ import unicode_literals
from datetime import date
from attest import TestBase, Tests, test
from django_attest import settings
from lib.models import Member, Guest, Meeting


suite = Tests()


class TestMember(TestBase):

    def __context__(self):
        self.member = Member(
            title='Sir',
            initials='M.E.',
            last_name='Palin',
            post_title='CBE FRGS',
            familiar_name='Michael'
        )
        yield
        del self.member

    @test
    def unicode_with_member_title(self):
        with settings(MEMBER_TITLE='Rotarian'):
            assert unicode(self.member) == 'Rotarian Michael Palin'

    @test
    def unicode_without_member_title(self):
        with settings(MEMBER_TITLE=None):
            assert unicode(self.member) == 'Michael Palin'

    @test
    def get_formal_name(self):
        assert self.member.get_formal_name() == 'Sir M.E. Palin CBE FRGS'

    # TODO: Test sync_email
    # def test_sync_email(self):
    #     ...


@suite.test
def guest_unicode():
    guest = Guest(
        title='Mr',
        first_name='Eric',
        last_name='Idle'
    )
    string = unicode(guest)
    assert string == 'Mr Eric Idle'


@suite.test
def meeting_unicode():
    meeting = Meeting(
        year=2013,
        month=2,
        date=date(2014, 3, 22),
        name='Meeting'
    )
    string = unicode(meeting)
    assert string == 'Meeting (March 2014)'


suite.register(TestMember)
suite = suite.test_suite
