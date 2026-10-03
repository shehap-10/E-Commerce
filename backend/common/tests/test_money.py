from decimal import Decimal

import pytest

from common.money import round_money


def test_rounds_half_up():
    assert round_money(Decimal("0.125")) == Decimal("0.13")


def test_rounds_down():
    assert round_money(Decimal("0.124")) == Decimal("0.12")


def test_accepts_integer():
    assert round_money(2) == Decimal("2.00")


def test_rounds_10_005():
    assert round_money(Decimal("10.005")) == Decimal("10.01")


def test_rejects_float():
    with pytest.raises(TypeError):
        round_money(0.1)


def test_rejects_bool():
    with pytest.raises(TypeError):
        round_money(True)


def test_rounds_negative_half_up():
    assert round_money(Decimal("-0.125")) == Decimal("-0.13")

