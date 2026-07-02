"""First-run configuration wizard.

If ``config.json`` is missing, this asks the user a few questions and writes the
file. It must not import :mod:`umauto.config` (that module reads config.json at
import time), so it only depends on :mod:`umauto.paths`.
"""

import json
import os

from .paths import resolve

CONFIG_PATH = resolve("config.json")

# Default values, also used as the fallback when a question is skipped.
DEFAULTS = {
    "steam": False,
    "steam_window_title": "umamusume",
    "device_id": "emulator-5554",
    "difficulty_tm": "medium",
    "daily_sales_buy": True,
    "alarm_clocks": True,
    "stars_pieces": True,
    "pleasing_parfait": True,
    "support_points": True,
    "racing_shoes": False,
    "sashes": True,
    "use_parfait": False,
    "cm_extra_run": True,
    "make_your_own_team": False,
}

# Daily-shop items asked only when shopping is enabled.
_SHOP_ITEMS = [
    ("stars_pieces", "Buy star pieces"),
    ("alarm_clocks", "Buy alarm clocks"),
    ("pleasing_parfait", "Buy pleasing parfaits"),
    ("support_points", "Buy support points"),
    ("racing_shoes", "Buy racing shoes"),
    ("sashes", "Buy sashes"),
]


def _ask_bool(prompt, default):
    suffix = "[Y/n]" if default else "[y/N]"
    truthy = {"y", "yes", "o", "oui"}
    falsy = {"n", "no", "non"}
    while True:
        answer = input(f"{prompt} {suffix} ").strip().lower()
        if not answer:
            return default
        if answer in truthy:
            return True
        if answer in falsy:
            return False
        print("  Please answer y or n.")


def _ask_str(prompt, default):
    answer = input(f"{prompt} [{default}] ").strip()
    return answer or default


def _ask_choice(prompt, options, default):
    joined = "/".join(options)
    while True:
        answer = input(f"{prompt} ({joined}) [{default}] ").strip().lower()
        if not answer:
            return default
        if answer in options:
            return answer
        print(f"  Please choose one of: {joined}.")


def _prompt_config():
    print("=" * 50)
    print("First run: let's create your config.json")
    print("(press Enter to keep the default shown in brackets)")
    print("=" * 50)

    config = dict(DEFAULTS)

    # --- Platform ---
    config["steam"] = _ask_bool("Play on Steam (PC)?", DEFAULTS["steam"])
    if config["steam"]:
        config["steam_window_title"] = _ask_str(
            "Steam window title", DEFAULTS["steam_window_title"]
        )
    else:
        config["device_id"] = _ask_str("ADB device id", DEFAULTS["device_id"])

    # --- Team Trials ---
    config["difficulty_tm"] = _ask_choice(
        "Team Trials difficulty", ["easy", "medium", "hard"], DEFAULTS["difficulty_tm"]
    )
    config["use_parfait"] = _ask_bool(
        "Use a parfait before each trial?", DEFAULTS["use_parfait"]
    )

    # --- Champions Meeting ---
    config["cm_extra_run"] = _ask_bool(
        "Do an extra Champions Meeting run?", DEFAULTS["cm_extra_run"]
    )
    config["make_your_own_team"] = _ask_bool(
        "Build your Champions Meeting team yourself?", DEFAULTS["make_your_own_team"]
    )

    # --- Daily shop ---
    config["daily_sales_buy"] = _ask_bool(
        "Buy daily-sale items after Team Trials?", DEFAULTS["daily_sales_buy"]
    )
    if config["daily_sales_buy"]:
        for key, prompt in _SHOP_ITEMS:
            config[key] = _ask_bool(f"  {prompt}?", DEFAULTS[key])

    return config


def _save(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def ensure_config():
    """Create config.json through an interactive wizard when it is missing."""
    if os.path.exists(CONFIG_PATH):
        return
    config = _prompt_config()
    _save(config)
    print(f"\nSaved {CONFIG_PATH}\n")
