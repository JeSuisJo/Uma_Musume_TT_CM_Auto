import tools as action
from tools import coords
import time

def run_trial():
    print("Running trial")
    while not action.compare_image(coords("quick_tt")["img"], coords("quick_tt")["region"], 0.9):
        if action.compare_image(coords("no_quick_tt")["img"], coords("no_quick_tt")["region"], 0.9):
            print("Quick mode activated")
            time.sleep(0.5)
            action.tap(*coords("quick_mode_tap")["tap"])

    time.sleep(0.5)
    action.tap(*coords("run_start")["tap"])

    while not action.compare_image(coords("race_finished")["img"], coords("race_finished")["region"], 0.9):
        time.sleep(0.5)
        action.tap(*coords("skip_tap")["tap"])

    print("Race finished")
    time.sleep(0.5)
    action.tap(*coords("race_finished")["tap"])
