from django.test import TestCase
from .user_signup.email_checker import get_email_report
from .user_signup.password_checker import get_password_strength
from .user_signup.username_checker import get_username_strength


class UserSignupTestCase(TestCase):
    def test_get_email_checker(self):
        self.assertEqual(get_email_report('xipersup@mgail.com'), '')
        self.assertEqual(get_email_report(
            'xianyu1121mgail.com'), 'Invalid email address.')

    def test_get_password_strength(self):
        self.assertEqual(get_password_strength(
            '12456'), ['The length of password should bettween 6 and 12 characters.',
                       'Password should contain at least one lowercase letter.',
                       'Password should contain at least one uppercase letter.']
        )
        self.assertEqual(get_password_strength(
            '1234563213213123123213131'), ['The length of password should bettween 6 and 12 characters.',
                                           'Password should contain at least one lowercase letter.',
                                           'Password should contain at least one uppercase letter.']
        )
        self.assertEqual(get_password_strength(
            '123456'), [
            'Password should contain at least one lowercase letter.',
            'Password should contain at least one uppercase letter.']
        )
        self.assertEqual(get_password_strength(
            'a123456'), ['Password should contain at least one uppercase letter.']
        )
        self.assertEqual(get_password_strength(
            'A123456'), ['Password should contain at least one lowercase letter.']
        )
        self.assertEqual(get_password_strength(
            'aaasdFeff'), ['Password should contain at least one digit.']
        )
        self.assertEqual(get_password_strength(
            'aA123456'), []
        )

    def test_get_username_strength(self):
        self.assertEqual(get_username_strength(
            '123'), 'The length of username should bettween 4 and 12 characters.')
        self.assertEqual(get_username_strength('1234563213213123123213131'),
                         'The length of username should bettween 4 and 12 characters.')
        self.assertEqual(get_username_strength('123456'), '')
        self.assertEqual(get_username_strength('a123456'), '')
        self.assertEqual(get_username_strength('A123456'), '')
        self.assertEqual(get_username_strength('aaasdFeff'), '')
        self.assertEqual(get_username_strength('aA123456'), '')
