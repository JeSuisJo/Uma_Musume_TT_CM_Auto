"""Daily Legends Race mode: run a single race with the configured champion."""

import os
import time

from ... import screen
from ...config import config
from ..common import handle_daily_sales
from .champions import COORD_BY_NAME, DEFAULT

# Champions in the bottom part of the list: the screen must be scrolled
# down before they become tappable.
_NEEDS_SCROLL = {
    "Mayano Top Gun",
    "Mejiro McQueen",
    "TM Opera O",
    "Super Creek",
    "Mejiro Ryan",
    "Silence Suzuka",
    "Gold Ship",
}


def run():
    os.system("cls")
    print("=" * 50)
    print("Uma Musume Daily Legends Race Auto")
    print("=" * 50)

    champion = config.get("daily_legends_champion", DEFAULT)
    champion_coord = COORD_BY_NAME.get(champion, COORD_BY_NAME[DEFAULT])

    print("Opening the daily program")
    screen.wait_from_home("daily_program_enter")
    screen.tap("daily_program_enter")
    time.sleep(1.5)
    screen.tap("daily_legends_enter")
    screen.wait("in_daily_legends")
    time.sleep(0.5)
    screen.swipe_to("dr_scroll_up")
    time.sleep(0.5)

    print(f"Selecting {champion}")
    if champion in _NEEDS_SCROLL:
        screen.swipe_to("dr_scroll")
        time.sleep(0.5)
        screen.tap(champion_coord)
    else:
        screen.tap(champion_coord)
    time.sleep(2)

    print("Starting the race")
    screen.tap("daily_legends_start")
    screen.wait("daily_race_start")
    screen.tap("daily_race_start")
    screen.wait("daily_race_confirm_runner")
    screen.tap("daily_race_confirm_runner")

    print("Running the race")
    screen.wait("dl_race")
    screen.tap("dl_race")
    time.sleep(0.5)
    if config.get("use_parfait"):
        print("Using a parfait")
        screen.tap("use_parfait")
        time.sleep(0.5)

    screen.tap("dl_run_race")
    screen.wait("dl_view_results")
    screen.tap("dl_view_results")

    while not screen.see("daily_legends_finish"):
        time.sleep(0.5)
        screen.tap("dl_next_not_found")

    print("Collecting the rewards")
    time.sleep(0.5)
    screen.tap("daily_legends_finish")
    screen.wait("dl_reward")
    screen.tap("dl_reward")
    time.sleep(2.5)
    handle_daily_sales()
    print("Daily legends race finished")