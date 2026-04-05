import tools as action
from tools import coords
import time

def launch_tt():
    print("Team Trials")
    while not action.compare_image(coords("in_trial")["img"], coords("in_trial")["region"], 0.9):
        time.sleep(0.5)
        if action.compare_image(coords("next_mondays")["img"], coords("next_mondays")["region"], 0.9):
            action.tap(*coords("next_mondays")["tap"])
            time.sleep(1)
    time.sleep(0.5)
    action.tap(*coords("launch_tt_tap")["tap"])
    time.sleep(1.8)
    if action.compare_image(coords("no_rp")["img"], coords("no_rp")["region"], 0.9):
        return True
