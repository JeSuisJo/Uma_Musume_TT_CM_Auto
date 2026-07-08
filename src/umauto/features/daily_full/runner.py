"""Full daily routine: Daily Races, then Daily Legends, then Team Trials.

Each step starts with ``wait_from_home``, so it re-syncs from the home screen
on its own even if the previous step left the game on another menu.
"""

from .. import daily_legends, daily_races, team_trials


def run():
    print("Full daily routine: Daily Races -> Daily Legends -> Team Trials")

    print("\n>>> Step 1/3: Daily Races")
    daily_races.run()

    print("\n>>> Step 2/3: Daily Legends")
    daily_legends.run()

    print("\n>>> Step 3/3: Team Trials")
    team_trials.run()

    print("\nFull daily routine finished")
