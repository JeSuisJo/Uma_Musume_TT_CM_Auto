import tools as action
from tools import coords
import json
import time

def setup_trial():
    print("Starting trial")
    c_ntt = coords("next_tt")
    action.wait_for_image(c_ntt["img"], c_ntt["region"], 0.9, 0.5)
    action.tap(*c_ntt["tap"])
    if json.load(open("config.json")).get("use_parfait") == True:
        time.sleep(1)
        print("Using parfait")
        action.tap(*coords("use_parfait")["tap"])

    time.sleep(1)
    action.tap(*coords("setup_confirm")["tap"])
