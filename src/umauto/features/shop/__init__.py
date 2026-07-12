"""Shop feature: buy daily-sale items, shared by every race mode.

Three buying strategies, chosen by the ``daily_sales_mode`` config key, one per
module so each file does exactly one thing:

* ``"all"``      buy every daily-sale item in one tap (:mod:`.buy_all`).
* ``"specific"`` buy only the items listed in ``shop_items`` config, found by
  template matching like the Daily Legends champion picker (:mod:`.buy_specific`).
* ``"off"``      don't buy anything.

Callers go through :func:`buy_sales` or :func:`handle_daily_sales` (:mod:`.dispatch`).
"""

from .buy_all import buy_all_sales
from .buy_specific import buy_specific_sales
from .dispatch import buy_sales, handle_daily_sales
from .mode import shop_mode

__all__ = [
    "buy_all_sales",
    "buy_sales",
    "buy_specific_sales",
    "handle_daily_sales",
    "shop_mode",
]
