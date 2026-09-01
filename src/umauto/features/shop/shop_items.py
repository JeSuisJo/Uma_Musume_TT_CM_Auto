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
