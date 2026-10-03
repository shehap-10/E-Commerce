from __future__ import annotations

from typing import Any

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import set_rollback

NON_FIELD_KEY = "non_field_errors"


class DomainError(Exception):
    """A business-rule failure that is safe to show to the client.

    The handler never reshapes unexpected errors, on purpose: a plain
    Python crash returns None so Django makes a plain 500 with no internals.
    """

    def __init__(self, code: str, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


def _flatten_errors(data: Any, prefix: str = "") -> dict[str, list[str]]:
    """Flatten DRF validation errors to {field_name: [messages]}.

    Rule: a non-dict payload (a string or a list of strings) is put under
    the single key "non_field_errors". Nested serializers get dotted names
    ("address.city"); list serializers get indexed names ("items.0.qty").
    """
    out: dict[str, list[str]] = {}

    def walk(node: Any, key: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{key}.{k}" if key else str(k))
        elif isinstance(node, (list, tuple)):
            if all(not isinstance(i, (dict, list, tuple)) for i in node):
                out.setdefault(key or NON_FIELD_KEY, []).extend(str(i) for i in node)
            else:
                for idx, item in enumerate(node):
                    if isinstance(item, (dict, list, tuple)):
                        walk(item, f"{key}.{idx}" if key else str(idx))
                    elif item:
                        out.setdefault(key or NON_FIELD_KEY, []).append(str(item))
        else:
            out.setdefault(key or NON_FIELD_KEY, []).append(str(node))

    walk(data, prefix)
    return out


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    # 1. Our own errors: skip DRF's handler, build the body ourselves.
    if isinstance(exc, DomainError):
        # DRF's handler would mark the transaction for rollback when
        # ATOMIC_REQUESTS is on; we skip it, so do it here (harmless otherwise).
        set_rollback()
        return Response({"code": exc.code, "detail": exc.message}, status=exc.status)

    # 2. Django's own errors: DRF converts them *inside* its handler, so
    #    `exc` here is still the Django one. Convert first to read the code.
    if isinstance(exc, Http404):
        exc = drf_exceptions.NotFound()
    elif isinstance(exc, DjangoPermissionDenied):
        exc = drf_exceptions.PermissionDenied()

    response = drf_exception_handler(exc, context)
    if response is None:
        # Unexpected error: do not touch it. Django makes a plain 500.
        return None

    # 3. Reshape the body, keeping status and headers (e.g. Retry-After).
    if isinstance(exc, drf_exceptions.ValidationError):
        response.data = {
            "code": "validation_error",
            "detail": "Validation failed.",
            "fields": _flatten_errors(response.data),
        }
    elif isinstance(exc, drf_exceptions.APIException):
        code = exc.get_codes()
        response.data = {
            "code": code if isinstance(code, str) else exc.default_code,
            "detail": str(exc.detail),
        }
    return response