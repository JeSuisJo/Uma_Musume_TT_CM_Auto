import os
import time

from ... import screen
from .difficulty import select_difficulty
from .finish import finish_run
from .launch import launch_trial
from .run import run_trial
from .setup import setup_trial


def run():
    run_number = 1
    need_launch = True
    while True:
        os.system("cls")
        print("=" * 50)
        print("Uma Musume Team Trials Auto")
        print(f"Run: {run_number}")
        print("=" * 50)

        if need_launch:
            screen.wait_from_home("tt_button")
            screen.tap("tt_button")
            if launch_trial():
                print("No more RP")
                screen.tap("no_rp_close")
                time.sleep(1)
                screen.tap("no_rp_confirm")
                return
            need_launch = False

        if not select_difficulty():
            setup_trial()
        run_trial()

        status = finish_run()
        if status == "no_rp":
            return
        if status == "home":
            need_launch = True
        run_number += 1
