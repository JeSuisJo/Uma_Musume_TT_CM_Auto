import tools as action
from tools import coords
import time
import json

def shop():
    action.tap(*coords("shop")["tap"])
    c_is = coords("in_shop")
    action.wait_for_image(c_is["img"], c_is["region"], 0.9, 0.5)

    cfg = json.load(open("config.json"))

    if cfg["stars_pieces"] == True:
        action.tap(*coords("stars_pieces_1")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_buy")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_confirm")["tap"])
        time.sleep(2)
        action.tap(*coords("stars_pieces_2")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_buy")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_confirm")["tap"])
        time.sleep(2)

    if cfg["alarm_clocks"] == True:
        action.tap(*coords("alarm_clocks")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_buy")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_confirm")["tap"])
        time.sleep(2)

    if cfg["pleasing_parfait"] == True:
        action.tap(*coords("pleasing_parfait")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_buy")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_confirm")["tap"])
        time.sleep(2)

    time.sleep(1)
    action.tap(*coords("shop_scroll")["tap"])
    time.sleep(1)
    action.tap(*coords("shop_scroll")["tap"])
    time.sleep(1)

    if cfg["racing_shoes"] == True:
        action.tap(*coords("racing_shoes")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_buy")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_confirm")["tap"])
        time.sleep(2)

    if cfg["support_points"] == True:
        action.tap(*coords("support_points")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_buy")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_confirm")["tap"])
        time.sleep(2)

    if cfg["sashes"] == True:
        action.tap(*coords("sashes")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_buy")["tap"])
        time.sleep(2)
        action.tap(*coords("shop_confirm")["tap"])
        time.sleep(2)

    time.sleep(1)
    action.tap(*coords("shop_close")["tap"])
    time.sleep(2)
    action.tap(*coords("shop_close_confirm")["tap"])
    time.sleep(2)
    action.tap(*coords("shop_back")["tap"])
    c_tt = coords("tt_button")
    action.wait_for_image(c_tt["img"], c_tt["region"], 0.9, 0.5)
    time.sleep(1)
    action.tap(*c_tt["tap"])
