import os
import time
import tools.adb as adb

def launch_tt():
    print("Team Trials")
    adb.wait_for_image("img/in_trial.png", (557, 893, 677, 931), 0.9, 0.5)
    time.sleep(0.5)
    adb.tap(407, 681)
    time.sleep(1.8)
    if adb.compare_image("img/no_rp.png", (476, 680, 585, 724), 0.9):
        return True