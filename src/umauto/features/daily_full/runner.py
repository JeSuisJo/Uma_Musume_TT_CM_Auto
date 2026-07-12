"""Full daily routine: Daily Races, then Daily Legends, then Team Trials.

Each step starts with ``wait_from_home``, so it re-syncs from the home screen
on its own even if the previous step left the game on another menu.
"""

from ...driver import StopScript
from .. import daily_legends, daily_races, team_trials


def _step(label, func):
    """Run one daily step, skipping it (not the whole routine) if it stops."""
    print(f"\n>>> {label}")
    try:
        func()
    except StopScript as exc:
        print(f"Skipping this step: {exc}")


def run():
    print("Full daily routine: Daily Races -> Daily Legends -> Team Trials")

    _step("Step 1/3: Daily Races", daily_races.run)
    _step("Step 2/3: Daily Legends", daily_legends.run)
    _step("Step 3/3: Team Trials", team_trials.run)

    print("\nFull daily routine finished")
