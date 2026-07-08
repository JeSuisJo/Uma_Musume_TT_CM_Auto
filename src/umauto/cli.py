"""Interactive menu: choose and launch an automation mode."""

import os

from .driver import driver
from .features import (
    champions_meeting,
    daily_full,
    daily_legends,
    daily_races,
    team_trials,
)

_MENU = """\
==================================================
Uma Musume TT CM Auto
==================================================
[1] Full Daily (Daily Races + Daily Legends + Team Trials)
[2] Team Trials
[3] Champions Meeting
[4] Daily Races
[5] Daily Legends Race
[0] Exit
"""


def _ask_int(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a number.")


def main():
    while True:
        os.system("cls")
        print(_MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            driver.focus()
            daily_full.run()
        elif choice == "2":
            driver.focus()
            team_trials.run()
        elif choice == "3":
            already_done = _ask_int("How many runs have you already done?: ")
            driver.focus()
            champions_meeting.run(already_done)
        elif choice == "4":
            driver.focus()
            daily_races.run()
        elif choice == "5":
            driver.focus()
            daily_legends.run()
        elif choice == "0":
            return
