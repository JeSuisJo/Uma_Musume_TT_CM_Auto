import tools as action
from tools import coords
import json
import time

def setup_trial():
    print("Starting trial")
    action.wait_for_image(coords("next_tt")["img"], coords("next_tt")["region"], 0.9, 0.5)
    action.tap(*coords("next_tt")["tap"])
    if json.load(open("config.json")).get("use_parfait") == True:
        time.sleep(1)
        print("Using parfait")
        action.tap(*coords("use_parfait")["tap"])

    time.sleep(1)
    action.tap(*coords("setup_confirm")["tap"])
