import tools as action
from tools import coords
import time

def run_trial():
    print("Running trial")
    c_q = coords("quick_tt")
    c_noq = coords("no_quick_tt")
    while not action.compare_image(c_q["img"], c_q["region"], 0.9):
        if action.compare_image(c_noq["img"], c_noq["region"], 0.9):
            print("Quick mode activated")
            time.sleep(0.5)
            action.tap(*coords("quick_mode_tap")["tap"])

    time.sleep(0.5)
    action.tap(*coords("run_start")["tap"])

    c_rf = coords("race_finished")
    while not action.compare_image(c_rf["img"], c_rf["region"], 0.9):
        time.sleep(0.5)
        action.tap(*coords("skip_tap")["tap"])

    print("Race finished")
    time.sleep(0.5)
    action.tap(*c_rf["tap"])
