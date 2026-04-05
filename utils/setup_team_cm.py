import tools as action
from tools import coords
import time

def setup_team(team):
    time.sleep(1.5)
    if not action.compare_image(coords("cm_auto_team")["img"], coords("cm_auto_team")["region"], 0.9):
        return

    if team == "1":
        input("Click enter when you have made your team")
    else:
        time.sleep(1)
        action.wait_for_image(coords("cm_auto_team")["img"], coords("cm_auto_team")["region"], 0.9, 0.5)
        action.tap(*coords("cm_auto_team")["tap"])
        time.sleep(1)
        action.wait_for_image(coords("cm_auto_team_ok")["img"], coords("cm_auto_team_ok")["region"], 0.9, 0.5)
        action.tap(*coords("cm_auto_team_ok")["tap"])
        time.sleep(1)

    action.tap(*coords("cm_team_selected")["tap"])
    time.sleep(1)
    action.tap(*coords("cm_confirm_registration")["tap"])
