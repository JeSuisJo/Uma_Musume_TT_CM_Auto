"""Default config values and the option lists offered by the wizard.

This module must stay importable *before* config.json exists, so it depends on
nothing else in the package. The champion and shop-item lists are duplicated
from :mod:`umauto.features.daily_legends.champions` and
:mod:`umauto.features.shop.shop_items`: the wizard runs before config.json
exists and therefore cannot import the ``features`` package (which reads
config.json at import time). Keep the three lists in sync.
"""

# Default values, also used as the fallback when a question is skipped.
DEFAULTS = {
    "steam": False,
    "steam_window_title": "umamusume",
    "device_id": "emulator-5554",
    "difficulty_tm": "medium",
    "daily_sales_mode": "all",
    "shop_items": [],
    "use_parfait_TT": False,
    "use_parfait_daily_legends": False,
    "cm_extra_run": True,
    "make_your_own_team": False,
    "daily_race_difficulty": "very_hard",
    "daily_race_reward": "money",
    "daily_legends_champion": "Special Week",
}

# Champions offered in the Daily Legends Race (display names).
DAILY_CHAMPIONS = [
    "El Condor Pasa",
    "Special Week",
    "Symboli Rudolf",
    "King Halo",
    "Taiki Shuttle",
    "Sakura Bakushin O",
    "Winning Ticket",
    "Vodka",
    "Tokai Teio",
    "Mayano Top Gun",
    "Mejiro McQueen",
    "TM Opera O",
    "Super Creek",
    "Mejiro Ryan",
    "Silence Suzuka",
    "Gold Ship",
]

# Shop items offered in the "specific" daily-sale buying mode (display names).
SHOP_ITEMS = [
    "Star Piece",
    "Alarm Clock",
    "Pleasing Parfait",
    "Sprint Shoes",
    "Mile Shoes",
    "Medium Shoes",
    "Long Shoes",
    "Dirt Shoes",
    "Support Points",
    "Sash",
]
