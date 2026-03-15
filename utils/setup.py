import tools.adb as adb
import json
import time

def setup_trial():
    print("Starting trial")
    adb.wait_for_image("img/next_tt.png", (364, 892, 430, 926), 0.9, 0.5)
    adb.tap(364, 892)
    if json.load(open("config.json")).get("use_parfait") == True:
        time.sleep(1)
        print("Using parfait")
        adb.tap(165, 486)
    
    time.sleep(1)
    adb.tap(526, 768)