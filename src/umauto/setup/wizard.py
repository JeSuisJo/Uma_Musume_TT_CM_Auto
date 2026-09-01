import json
import os

from ..paths import resolve
from .defaults import DAILY_CHAMPIONS, DEFAULTS, SHOP_ITEMS
from .prompts import (
    ask_bool,
    ask_choice,
    ask_from_list,
    ask_multi_from_list,
    ask_str,
)

CONFIG_PATH = resolve("config.json")


class _Question:
    def __init__(self, key, ask, when=None):
        self.key = key
        self.ask = ask
        self.when = when

    def applies(self, config):
        return self.when is None or self.when(config)


_QUESTIONS = [
    _Question("steam", lambda c: ask_bool("Play on Steam (PC)?", DEFAULTS["steam"])),
    _Question(
        "steam_window_title",
        lambda c: ask_str("Steam window title", DEFAULTS["steam_window_title"]),
        when=lambda c: c.get("steam"),
    ),
    _Question(
        "difficulty_tm",
        lambda c: ask_choice(
            "Team Trials difficulty",
            ["easy", "medium", "hard"],
            DEFAULTS["difficulty_tm"],
        ),
    ),
    _Question(
        "use_parfait_TT",
        lambda c: ask_bool(
            "Use a parfait before each Team Trials run?",
            c.get("use_parfait", DEFAULTS["use_parfait_TT"]),
        ),
    ),
    _Question(
        "use_parfait_daily_legends",
        lambda c: ask_bool(
            "Use a parfait before each Daily Legends race?",
            c.get("use_parfait", DEFAULTS["use_parfait_daily_legends"]),
        ),
    ),
    _Question(
        "cm_extra_run",
        lambda c: ask_bool(
            "Do an extra Champions Meeting run?", DEFAULTS["cm_extra_run"]
        ),
    ),
    _Question(
        "make_your_own_team",
        lambda c: ask_bool(
            "Build your Champions Meeting team yourself?",
            DEFAULTS["make_your_own_team"],
        ),
    ),
    _Question(
        "daily_sales_mode",
        lambda c: ask_choice(
            "Daily shop buying (all = everything, specific = chosen items, "
            "off = nothing)",
            ["all", "specific", "off"],
            DEFAULTS["daily_sales_mode"],
        ),
    ),
    _Question(
        "shop_items",
        lambda c: ask_multi_from_list(
            "Which shop items should be bought?", SHOP_ITEMS, DEFAULTS["shop_items"]
        ),
        when=lambda c: c.get("daily_sales_mode") == "specific",
    ),
    _Question(
        "daily_race_difficulty",
        lambda c: ask_choice(
            "Daily Races difficulty",
            ["easy", "normal", "hard", "very_hard"],
            DEFAULTS["daily_race_difficulty"],
        ),
    ),
    _Question(
        "daily_race_reward",
        lambda c: ask_choice(
            "Daily Races reward", ["money", "support"], DEFAULTS["daily_race_reward"]
        ),
    ),
    _Question(
        "daily_legends_champion",
        lambda c: ask_from_list(
            "Daily Legends Race champion:",
            DAILY_CHAMPIONS,
            DEFAULTS["daily_legends_champion"],
        ),
    ),
]


def _prompt_config():
    print("=" * 50)
    print("First run: let's create your config.json")
    print("(press Enter to keep the default shown in brackets)")
    print("=" * 50)

    config = dict(DEFAULTS)
    for question in _QUESTIONS:
        if question.applies(config):
            config[question.key] = question.ask(config)
    return config


def _migrate(existing):
    config = dict(existing)
    added = []
    for question in _QUESTIONS:
        if question.key in config or not question.applies(config):
            continue
        if not added:
            print("=" * 50)
            print("Update: new options were added since your last config.")
            print("Let's set them (press Enter to keep the default).")
            print("=" * 50)
        config[question.key] = question.ask(config)
        added.append(question.key)

    if not added:
        return False
    _save(config)
    print(f"\nUpdated {CONFIG_PATH} with: {', '.join(added)}\n")
    return True


def _save(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def ensure_config():
    if not os.path.exists(CONFIG_PATH):
        config = _prompt_config()
        _save(config)
        print(f"\nSaved {CONFIG_PATH}\n")
        return

    with open(CONFIG_PATH, encoding="utf-8") as f:
        existing = json.load(f)
    _migrate(existing)
