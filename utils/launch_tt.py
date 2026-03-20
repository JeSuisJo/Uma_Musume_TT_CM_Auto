import os
import time
import tools as action
from tools import coords

def launch_tt():
    print("Team Trials")
    c_trial = coords("in_trial")
    c_mon = coords("next_mondays")
    while not action.compare_image(c_trial["img"], c_trial["region"], 0.9):
        time.sleep(0.5)
        if action.compare_image(c_mon["img"], c_mon["region"], 0.9):
            action.tap(*c_mon["tap"])
            time.sleep(1)
    time.sleep(0.5)
    action.tap(*coords("launch_tt_tap")["tap"])
    time.sleep(1.8)
    c_norp = coords("no_rp")
    if action.compare_image(c_norp["img"], c_norp["region"], 0.9):
        return True
