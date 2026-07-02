"""Register the team for a Champions Meeting run."""

import time

from ... import screen


def setup_team(make_own_team):
    time.sleep(1.5)
    if not screen.see("cm_auto_team"):
        return

    if screen.see("no_uma_in_cm"):
        if make_own_team:
            input("Press Enter once your team is ready")
        else:
            time.sleep(1)
            screen.tap("cm_auto_team")
            time.sleep(1)
            screen.wait("cm_auto_team_ok")
            screen.tap("cm_auto_team_ok")
            time.sleep(1)

    screen.tap("cm_team_selected")
    time.sleep(1)
    screen.tap("cm_confirm_registration")
