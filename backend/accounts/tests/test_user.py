import pytest
from django.core.management import call_command
from django.db import IntegrityError,connection, transaction

from accounts.models import User
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_manager_creates_users_and_rejects_empty_email():
    user = User.objects.create_user("Shopper@EXAMPLE.COM", "long-test-password")
    admin = User.objects.create_superuser("Admin@EXAMPLE.COM", "long-test-password")

    assert user.email == "Shopper@example.com"
    assert user.check_password("long-test-password")
    assert not user.is_staff
    assert admin.email == "Admin@example.com"
    assert admin.is_staff
    assert admin.is_superuser

    with pytest.raises(ValueError, match="email"):
        User.objects.create_user("", "long-test-password")
    with pytest.raises(ValueError, match="email"):
        User.objects.create_superuser("", "long-test-password")


@pytest.mark.django_db
def test_database_rejects_email_duplicate_ignoring_case():
    UserFactory.create(email="A@EXAMPLE.COM")

    with pytest.raises(IntegrityError), transaction.atomic():
        User.objects.create(email="a@example.com")

@pytest.mark.django_db
def test_createsuperuser_command_uses_email_without_username(monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "long-test-password")

    call_command(
        "createsuperuser",
        email="admin@example.com",
        interactive=False,
        verbosity=0,
    )

    user = User.objects.get(email="admin@example.com")
    assert user.is_staff
    assert user.is_superuser


@pytest.mark.django_db
def test_database_is_postgresql():
    assert connection.vendor == "postgresql"