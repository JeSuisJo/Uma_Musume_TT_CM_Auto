"""Configuration wizard: create config.json, or backfill new keys into it.

It must not import :mod:`umauto.config` (that module reads config.json at import
time), so it only depends on :mod:`umauto.paths` and this package's own
:mod:`.defaults` / :mod:`.prompts`.

The questions live in one ordered, declarative list (:data:`_QUESTIONS`) shared
by two entry points:

* a **fresh install** (no config.json) asks every applicable question;
* an **upgrade** (config.json exists but predates keys added in a new release)
  asks *only* the missing ones, then rewrites the file -- so users who update
  get prompted for the new options instead of silently running on defaults.

To expose a new option, add one :class:`_Question` row (and its default in
:mod:`.defaults`); both flows pick it up automatically.
"""

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
    """One config key, how to ask for it, and when it is relevant.

    ``ask`` receives the config answered so far, so a question can seed its
    default from another key -- e.g. the split ``use_parfait_TT`` /
    ``use_parfait_daily_legends`` questions default to the legacy single
    ``use_parfait`` value when upgrading. ``when`` gates conditional keys against
    that same config (e.g. ``shop_items`` is only asked when ``daily_sales_mode``
    is ``"specific"``). Because both flows walk :data:`_QUESTIONS` in order, a
    guard or default can safely read a key asked earlier in the list.
    """

    def __init__(self, key, ask, when=None):
        self.key = key
        self.ask = ask
        self.when = when

    def applies(self, config):
        return self.when is None or self.when(config)


# Ordered so every guard's dependency is asked before it (steam before the
# steam/adb split, daily_sales_mode before shop_items).
_QUESTIONS = [
    _Question("steam", lambda c: ask_bool("Play on Steam (PC)?", DEFAULTS["steam"])),
    _Question(
        "steam_window_title",
        lambda c: ask_str("Steam window title", DEFAULTS["steam_window_title"]),
        when=lambda c: c.get("steam"),
    ),
    # device_id is not asked: it is detected (and saved) automatically at run
    # start by the ADB driver -- see AdbDriver.ensure_ready. The default from
    # DEFAULTS lands in config.json as the initial cached value.
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
        # Default seeded from the legacy single ``use_parfait`` key so a user
        # upgrading from before the split keeps their old choice.
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

    # Start from the defaults so skipped conditional keys (e.g. device_id for a
    # Steam user) still land in the file with a harmless value.
    config = dict(DEFAULTS)
    for question in _QUESTIONS:
        if question.applies(config):
            config[question.key] = question.ask(config)
    return config


def _migrate(existing):
    """Ask only for keys a new release added, then rewrite config.json.

    Walks :data:`_QUESTIONS` against the user's current config: a question is
    asked only when its key is absent *and* it applies. Re-checking ``applies``
    as answers come in handles cascades -- answering a newly added
    ``daily_sales_mode`` with ``"specific"`` makes the also-missing
    ``shop_items`` become relevant and get asked too. Returns True if anything
    was added.
    """
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
    """Create config.json on a fresh install, or backfill new keys on upgrade."""
    if not os.path.exists(CONFIG_PATH):
        config = _prompt_config()
        _save(config)
        print(f"\nSaved {CONFIG_PATH}\n")
        return

    with open(CONFIG_PATH, encoding="utf-8") as f:
        existing = json.load(f)
    _migrate(existing)
