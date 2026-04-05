import tools as action
from tools import coords
import time

def launch_cm():
    print("Going to the Champions Meeting")
    action.wait_for_image(coords("go_to_cm")["img"], coords("go_to_cm")["region"], 0.9, 0.5)
    action.tap(*coords("go_to_cm")["tap"])
    time.sleep(0.5)
    while not action.compare_image(coords("in_cm")["img"], coords("in_cm")["region"], 0.9):
        time.sleep(0.5)
        action.tap(*coords("cm_popup_close")["tap"])
    print("In the Champions Meeting")
