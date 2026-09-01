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
    prepare: Optional[Callable] = None


def _ask_int(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a number.")


def _prepare_champions_meeting():
    return (_ask_int("How many runs have you already done?: "),)


FEATURES = {
    "1": Feature("Full Daily", daily_full.run),
    "2": Feature("Team Trials", team_trials.run),
    "3": Feature("Champions Meeting", champions_meeting.run, prepare=_prepare_champions_meeting),
    "4": Feature("Daily Races", daily_races.run),
    "5": Feature("Daily Legends Race", daily_legends.run),
}
