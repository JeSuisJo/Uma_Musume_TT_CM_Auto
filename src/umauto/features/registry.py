"""Central registry of automation modes shown in the menu.

Adding a feature here is enough for it to appear in the CLI menu: no need to
touch the menu loop. Each entry maps a menu key to a `Feature` describing its
label, its `run` entry point, and an optional `prepare` step that collects
input before the run (e.g. asking how many runs are already done).
"""

from dataclasses import dataclass
from typing import Callable, Optional

from . import (
    champions_meeting,
    daily_full,
    daily_legends,
    daily_races,
    team_trials,
)


@dataclass
class Feature:
    label: str
    run: Callable
    # Runs before `run`, after the menu choice; returns the args passed to
    # `run`. Used for modes that need extra input (returns a tuple/list).
    prepare: Optional[Callable] = None


def _ask_int(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a number.")


def _prepare_champions_meeting():
    return (_ask_int("How many runs have you already done?: "),)


# Keys are the strings typed at the menu; insertion order defines menu order.
FEATURES = {
    "1": Feature("Full Daily", daily_full.run),
    "2": Feature("Team Trials", team_trials.run),
    "3": Feature("Champions Meeting", champions_meeting.run, prepare=_prepare_champions_meeting),
    "4": Feature("Daily Races", daily_races.run),
    "5": Feature("Daily Legends Race", daily_legends.run),
}
