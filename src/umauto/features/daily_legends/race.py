"""Start and run the selected Daily Legends race, then collect the rewards."""

import time

from ... import screen
from ...config import config
from ..shop import handle_daily_sales


def run_race():
    """Run the race (optionally using a parfait) and collect its rewards."""
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
    if config.get("use_parfait_daily_legends"):
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

    screen.wait_any("in_daily_legends", "daily_legends_enter")
    screen.tap("home")
