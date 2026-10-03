import factory
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory

from accounts.models import User


class UserFactory(DjangoModelFactory):
    email = factory.Sequence(lambda number: f"user{number}@example.com")
    password = factory.LazyFunction(lambda: make_password("test-password"))

    class Meta:
        model = User