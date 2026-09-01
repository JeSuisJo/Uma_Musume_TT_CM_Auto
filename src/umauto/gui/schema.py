from ..setup.defaults import DAILY_CHAMPIONS, DEFAULTS, SHOP_ITEMS

FIELDS = [
    {
        "key": "steam",
        "type": "bool",
        "label": "Play on Steam (PC)",
        "help": "Turn off for an Android emulator driven by ADB.",
    },
    {
        "key": "steam_window_title",
        "type": "text",
        "label": "Steam window title",
        "when": {"steam": True},
    },
    {
        "key": "device_id",
        "type": "info",
        "label": "ADB device",
        "help": "Detected automatically before each run.",
        "when": {"steam": False},
    },
    {
        "key": "difficulty_tm",
        "type": "choice",
        "label": "Team Trials difficulty",
        "options": ["easy", "medium", "hard"],
    },
    {
        "key": "use_parfait_TT",
        "type": "bool",
        "label": "Use a parfait before each Team Trials run",
    },
    {
        "key": "use_parfait_daily_legends",
        "type": "bool",
        "label": "Use a parfait before each Daily Legends race",
    },
    {
        "key": "cm_extra_run",
        "type": "bool",
        "label": "Do an extra Champions Meeting run",
    },
    {
        "key": "make_your_own_team",
        "type": "bool",
        "label": "Build your Champions Meeting team yourself",
        "help": "The app pauses so you can set up your team.",
    },
    {
        "key": "daily_sales_mode",
        "type": "choice",
        "label": "Daily shop buying",
        "options": ["all", "specific", "off"],
        "option_labels": {
            "all": "Buy everything",
            "specific": "Chosen items",
            "off": "Buy nothing",
        },
    },
    {
        "key": "shop_items",
        "type": "multichoice",
        "label": "Items to buy",
        "options": SHOP_ITEMS,
        "when": {"daily_sales_mode": "specific"},
    },
    {
        "key": "daily_race_difficulty",
        "type": "choice",
        "label": "Daily Races difficulty",
        "options": ["easy", "normal", "hard", "very_hard"],
        "option_labels": {"very_hard": "very hard"},
    },
    {
        "key": "daily_race_reward",
        "type": "choice",
        "label": "Daily Races reward",
        "options": ["money", "support"],
        "option_labels": {"money": "Money", "support": "Support points"},
    },
    {
        "key": "daily_legends_champion",
        "type": "choice",
        "label": "Daily Legends champion",
        "options": DAILY_CHAMPIONS,
    },
    {
        "key": "window_on_top",
        "type": "bool",
        "label": "Keep the app window on top while a mode runs",
        "help": "Floats over the game once a mode is launched, on an empty corner"
                " (letterbox bar). Outside a run the window behaves normally.",
        "when": {"steam": True},
    },
    {
        "key": "dark_mode",
        "type": "bool",
        "label": "Dark mode",
        "help": "Switch the app to the dark arcade theme.",
    },
]


_GUI_DEFAULTS = {
    "window_on_top": False,
    "dark_mode": False,
}


def defaults():
    return {**DEFAULTS, **_GUI_DEFAULTS}
