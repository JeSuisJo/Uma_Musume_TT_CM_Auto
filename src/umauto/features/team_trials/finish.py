"""Handle post-race popups, optional shopping, then race again or stop."""

import time

from ... import screen
from ..shop import buy_sales

_POPUPS = ("highscore", "story_unlocked", "next_go_to_reward", "next_reward")


def finish_run():
    """Clear post-race popups, then tap 'race again' to start another run.

    Returns one of:

    * ``"again"`` -- race points remain; 'race again' brought the game back to
      the difficulty selection screen, ready for the next loop.
    * ``"no_rp"`` -- race points ran out; the no-RP popup was dismissed and the
      game sent home. The caller should stop.
    * ``"home"`` -- the daily shop appeared and a purchase ran, which leaves the
      game on the home screen. The caller must re-enter Team Trials from there.
    """
    while not screen.see("race_again"):
        for popup in _POPUPS:
            # ``story_unlocked`` can appear at slightly different positions, so
            # find it anywhere in its region (template match) instead of a fixed
            # pixel-for-pixel comparison, and tap wherever it was found.
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

    # After 'race again' the game returns to the selection screen, unless race
    # points are out -- then the no-RP popup shows up instead.
    while True:
        if screen.see_any("in_selection", "in_selection_refresh"):
            return "again"
        if screen.see("no_rp"):
            _no_rp_exit()
            return "no_rp"
        time.sleep(0.5)


def _no_rp_exit():
    """Dismiss the no-RP popup, close the run and go back to the home screen."""
    print("No more RP")
    time.sleep(0.5)
    screen.tap("no_rp_close")
    time.sleep(1)
    screen.tap("finish_run")  # the "next" button
    screen.wait("in_trial")
    time.sleep(0.5)
    screen.tap("home")
