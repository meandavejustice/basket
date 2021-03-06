from django.test import TestCase

from flanker.addresslib.address import EmailAddress
from mock import patch
from nose.tools import ok_, eq_

from news.email import get_valid_email


@patch('news.email.validate.suggest_alternate')
@patch('news.email.address.validate_address')
class TestGetValidEmail(TestCase):
    email = 'dude@example.com'

    def test_valid_email(self, mock_validate, mock_suggest):
        """Should allow a valid email to pass through."""
        mock_suggest.return_value = None
        mock_validate.return_value = self.email
        result, is_suggestion = get_valid_email(self.email)
        ok_(not is_suggestion)
        eq_(result, self.email)

    def test_no_email(self, mock_validate, mock_suggest):
        """Should return None for a None value."""
        result, is_suggestion = get_valid_email(None)
        ok_(result is None)
        ok_(not mock_validate.called)
        ok_(not mock_suggest.called)

    def test_misspelled_email(self, mock_validate, mock_suggest):
        """Should correct a misspelled domain and pass it back."""
        email2 = 'dude2@example.com'
        mock_suggest.return_value = email2
        mock_validate.return_value = EmailAddress('', email2)
        result, is_suggestion = get_valid_email(self.email)
        ok_(is_suggestion)
        # should return a string, not the EmailAddress instance
        ok_(isinstance(result, basestring))
        eq_(result, email2)

    def test_invalid_email(self, mock_validate, mock_suggest):
        """Should return None for an invalid address."""
        mock_suggest.return_value = None
        mock_validate.return_value = None
        result = get_valid_email(self.email)[0]
        ok_(not result)
