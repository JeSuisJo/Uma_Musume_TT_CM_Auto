import time

from ... import screen
from ..shop import buy_sales

_POPUPS = ("highscore", "story_unlocked", "next_go_to_reward", "next_reward")


def finish_run():
    while not screen.see("race_again"):
        for popup in _POPUPS:
            if popup == "story_unlocked":
                if screen.see_template(popup):
                    time.sleep(0.5)
                    screen.tap_template(popup)
                continue

            if screen.see(popup):
                time.sleep(0.5)
                screen.tap(popup)

        if screen.see("shop"):
            time.sleep(0.5)
            if buy_sales():
                return "home"
            screen.tap("shop_cancel")
            time.sleep(1)

    print("Race again")
    time.sleep(0.8)
    screen.tap("race_again")

    while True:
        if screen.see_any("in_selection", "in_selection_refresh"):
            return "again"
        if screen.see("no_rp"):
            _no_rp_exit()
            return "no_rp"
        time.sleep(0.5)


def _no_rp_exit():
    print("No more RP")
    time.sleep(0.5)
    screen.tap("no_rp_close")
    time.sleep(1)
    screen.tap("finish_run")
    screen.wait("in_trial")
    time.sleep(0.5)
    screen.tap("home")
