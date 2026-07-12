"""Shop items purchasable in the "specific" daily-sale buying mode.

Mirrors the Daily Legends champions setup (:mod:`umauto.features.daily_legends.
champions`): the config stores a list of item display names, and
``COORD_BY_NAME`` maps each name to the coordinate entry whose template is
searched for (and tapped) inside the shop's scrollable item region.

To add a shop item you edit three things, exactly like a Daily Legends champion:

1. Add a ``(display name, coordinate name)`` row to ``SHOP_ITEMS`` below, and
   mirror the display name in :data:`umauto.setup.defaults.SHOP_ITEMS` so the
   setup wizard offers it (a test keeps the two lists in sync).
2. Add the matching entry to ``coords/shop.json`` (a ``region`` covering the
   shop's scrollable item list, and an ``img`` template of just that item's
   icon).
3. Drop the template PNG at the ``img`` path referenced by that entry
   (``img/android/<name>.png`` and, for the Steam build,
   ``img/steam/<name>.png``).

Capture a template image for each item before enabling the "specific" mode.
"""

# (display name, coordinate name) in the order shown in the shop.
SHOP_ITEMS = [
    ("Star Piece", "shop_star_piece"),
    ("Alarm Clock", "shop_alarm_clock"),
    ("Pleasing Parfait", "shop_pleasing_parfait"),
    ("Sprint Shoes", "shop_sprint_shoes"),
    ("Mile Shoes", "shop_mile_shoes"),
    ("Medium Shoes", "shop_medium_shoes"),
    ("Long Shoes", "shop_long_shoes"),
    ("Dirt Shoes", "shop_dirt_shoes"),
    ("Support Points", "shop_support_points"),
    ("Sash", "shop_sash"),
]

NAMES = [name for name, _ in SHOP_ITEMS]
COORD_BY_NAME = {name: coord for name, coord in SHOP_ITEMS}
