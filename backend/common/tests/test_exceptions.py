import pytest

from django.conf import settings
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404

from rest_framework import exceptions as drf
from rest_framework.settings import api_settings

from common.exceptions import DomainError, api_exception_handler


CTX = {"view": None, "request": None}


def handle(exc):
    return api_exception_handler(exc, CTX)


def test_domain_error_body_and_status():
    r = handle(DomainError("out_of_stock", "No stock left", 409))
    assert r.status_code == 409
    assert r.data == {"code": "out_of_stock", "detail": "No stock left"}
    assert "fields" not in r.data


def test_validation_error_dict():
    r = handle(
        drf.ValidationError(
            {"email": ["Bad email"], "name": ["Required"]}
        )
    )
    assert r.status_code == 400
    assert r.data["code"] == "validation_error"
    assert r.data["fields"] == {
        "email": ["Bad email"],
        "name": ["Required"],
    }


@pytest.mark.parametrize(
    "payload",
    ["Something is wrong", ["a", "b"]],
)
def test_validation_error_non_dict_uses_non_field_errors(payload):
    r = handle(drf.ValidationError(payload))
    assert isinstance(r.data["fields"], dict)
    assert "non_field_errors" in r.data["fields"]


def test_validation_error_nested_gets_dotted_names():
    r = handle(
        drf.ValidationError(
            {"address": {"city": ["Required"]}}
        )
    )
    assert r.data["fields"] == {
        "address.city": ["Required"]
    }


def test_not_authenticated():
    r = handle(drf.NotAuthenticated())
    assert r.status_code == 401
    assert r.data["code"] == "not_authenticated"
    assert "detail" in r.data


def test_permission_denied():
    r = handle(drf.PermissionDenied())
    assert r.status_code == 403
    assert r.data["code"] == "permission_denied"


@pytest.mark.parametrize(
    "exc",
    [drf.NotFound(), Http404()],
)
def test_not_found_variants(exc):
    r = handle(exc)
    assert r.status_code == 404
    assert r.data["code"] == "not_found"


def test_django_permission_denied_converted():
    r = handle(DjangoPermissionDenied())
    assert r.status_code == 403
    assert r.data["code"] == "permission_denied"


def test_throttled_keeps_retry_after():
    r = handle(drf.Throttled(wait=30))
    assert r.status_code == 429
    assert r.data["code"] == "throttled"
    assert r["Retry-After"] == "30"


def test_unexpected_error_returns_none():
    secret = "db password is hunter2"
    assert handle(ValueError(secret)) is None


def test_setting_points_to_handler():
    assert api_settings.EXCEPTION_HANDLER is api_exception_handler

