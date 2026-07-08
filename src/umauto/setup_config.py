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
    "use_parfait": False,
    "cm_extra_run": True,
    "make_your_own_team": False,
    "daily_race_difficulty": "very_hard",
    "daily_race_reward": "money",
    "daily_legends_champion": "Special Week",
}


# Champions offered in the Daily Legends Race (display names).
_DAILY_CHAMPIONS = [
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


def _ask_from_list(prompt, options, default):
    default_index = options.index(default) + 1 if default in options else 1
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"  [{i}] {option}")
        answer = input(f"Choice [{default_index}]: ").strip()
        if not answer:
            return options[default_index - 1]
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        print(f"  Please enter a number between 1 and {len(options)}.")


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
        "Buy all daily-sale items after Team Trials?", DEFAULTS["daily_sales_buy"]
    )

    # --- Daily Races ---
    config["daily_race_difficulty"] = _ask_choice(
        "Daily Races difficulty",
        ["easy", "normal", "hard", "very_hard"],
        DEFAULTS["daily_race_difficulty"],
    )
    config["daily_race_reward"] = _ask_choice(
        "Daily Races reward", ["money", "support"], DEFAULTS["daily_race_reward"]
    )

    # --- Daily Legends Race ---
    config["daily_legends_champion"] = _ask_from_list(
        "Daily Legends Race champion:",
        _DAILY_CHAMPIONS,
        DEFAULTS["daily_legends_champion"],
    )

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
