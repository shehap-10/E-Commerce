from decimal import Decimal, ROUND_HALF_UP


def round_money(value: int | Decimal) -> Decimal:
	"""Round an integer or Decimal monetary value to two decimal places."""
	if isinstance(value, bool) or not isinstance(value, (int, Decimal)):
		raise TypeError("value must be an int or Decimal")

	return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
