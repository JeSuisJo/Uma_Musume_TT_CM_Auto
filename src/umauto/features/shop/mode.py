"""Resolve the configured shop buying mode."""

from ...config import config


def shop_mode():
    """Return the configured shop mode: ``"all"``, ``"specific"`` or ``"off"``.

    Falls back to the legacy ``daily_sales_buy`` boolean for configs written
    before the mode key existed.
    """
    mode = config.get("daily_sales_mode")
    if mode is not None:
        return mode
    return "all" if config.get("daily_sales_buy") else "off"
