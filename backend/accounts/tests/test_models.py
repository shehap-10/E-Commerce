from django.db import IntegrityError, transaction
from django.test import TestCase

from accounts.models import User


class UserManagerTests(TestCase):
    def test_create_user_normalizes_email_and_hashes_password(self):
        user = User.objects.create_user("Shopper@Example.com", "long-test-password")

        self.assertEqual(user.email, "shopper@example.com")
        self.assertTrue(user.check_password("long-test-password"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_email_is_case_insensitively_unique(self):
        User.objects.create_user("shopper@example.com", "long-test-password")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user("SHOPPER@EXAMPLE.COM", "another-password")

    def test_create_superuser_sets_staff_and_superuser_flags(self):
        user = User.objects.create_superuser("admin@example.com", "long-test-password")

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)