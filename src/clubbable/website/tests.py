from contextlib import contextmanager
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


@contextmanager
def user_context():
    details = {'username': 'testy', 'password': 's3cr3t'}
    user = User(username=details['username'])
    user.set_password(details['password'])
    user.save()
    details['id'] = user.id
    try:
        yield details
    finally:
        user.delete()


class DashboardViewTests(TestCase):

    def test_dashboard_unauthenticated(self):
        """
        The dashboard view should redirect if the user isn't authenticated
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated(self):
        """
        The dashboard view should return status 200 if user is authenticated
        """
        with user_context() as user:
            self.client.post(
                reverse('login'),
                {'username': user['username'],
                 'password': user['password']})
            # Check login was successful
            self.assertIn('_auth_user_id', self.client.session)
            self.assertEqual(
                self.client.session['_auth_user_id'], user['id'])

            response = self.client.get(reverse('dashboard'))
            self.assertEqual(response.status_code, 200)
