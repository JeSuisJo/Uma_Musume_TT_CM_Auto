"""Interactive menu: choose and launch an automation mode."""

import os

from .driver import driver
from .features import champions_meeting, team_trials

_MENU = """\
==================================================
Uma Musume TT CM Auto
==================================================
[1] Team Trials
[2] Champions Meeting
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
            team_trials.run()
        elif choice == "2":
            already_done = _ask_int("How many runs have you already done?: ")
            driver.focus()
            champions_meeting.run(already_done)
        elif choice == "0":
            return
