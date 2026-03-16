import tools.adb as adb
import time
import json

def shop():
    adb.tap(489, 679)
    adb.wait_for_image("img/in_shop.png", (570, 451, 651, 485), 0.9, 0.5)
    if json.load(open("config.json"))["stars_pieces"] == True:
        adb.tap(608, 467)
        time.sleep(1)
        adb.tap(527, 775)
        time.sleep(1)
        adb.tap(407, 703)
        time.sleep(1)
        adb.tap(616, 601)
        time.sleep(1)
        adb.tap(527, 775)
        time.sleep(1)
        adb.tap(407, 703)
        time.sleep(1)

    if json.load(open("config.json"))["alarm_clocks"] == True:
        adb.tap(616, 733)
        time.sleep(1)
        adb.tap(527, 775)
        time.sleep(1)
        adb.tap(407, 703)
        time.sleep(1)

    if json.load(open("config.json"))["pleasing_parfait"] == True:
        adb.tap(617, 844)
        time.sleep(1)
        adb.tap(527, 775)
        time.sleep(1)
        adb.tap(407, 703)
        time.sleep(1)

    time.sleep(1)
    adb.tap(688, 842)
    time.sleep(0.5)

    if json.load(open("config.json"))["racing_shoes"] == True:
        adb.tap(609, 570)
        time.sleep(1)
        adb.tap(527, 775)
        time.sleep(1)
        adb.tap(407, 703)
        time.sleep(1)

    if json.load(open("config.json"))["support_points"] == True:
        adb.tap(612, 683)
        time.sleep(1)
        adb.tap(527, 775)
        time.sleep(1)
        adb.tap(407, 703)
        time.sleep(1)

    if json.load(open("config.json"))["sashes"] == True:
        adb.tap(622, 798)
        time.sleep(1)
        adb.tap(527, 775)
        time.sleep(1)
        adb.tap(407, 703)
        time.sleep(1)

    # ------------------ Ferme le shop ------------------
    time.sleep(0.5)
    adb.tap(394, 911)
    time.sleep(1)
    adb.tap(532, 702)
    time.sleep(1)
    adb.tap(538, 1023)
    adb.wait_for_image("img/tt.png", (204, 759, 341, 792), 0.9, 0.5)
    time.sleep(0.5)
    adb.tap(204, 759)