import tools as action
from tools import coords
import time
import json

def _buy_item(slot_y, slot_x):
    action.tap(slot_x, slot_y)
    time.sleep(1.5)
    action.tap(*coords("shop_buy")["tap"])
    time.sleep(1.5)
    action.tap(*coords("shop_confirm")["tap"])
    time.sleep(1.5)

def shop():
    # action.tap(*coords("shop")["tap"])
    c_is = coords("in_shop")
    action.wait_for_image(c_is["img"], c_is["region"], 0.9, 0.5)

    cfg = json.load(open("config.json"))
    use_steam = cfg.get("steam", False)

    # Page 1 : 4 slots visibles | Page 2 : 3 slots visibles après scroll
    if use_steam:
        p1_slots_y = [467, 594, 734, 847]
        p1_x = 764
        p2_slots_y = [565, 679, 800]
        p2_x = 766
    else:
        p1_slots_y = [467, 601, 733, 844]
        p1_x = 615
        p2_slots_y = [570, 683, 798]
        p2_x = 614

    # Tous les items dans l'ordre original (index 0 à 6)
    all_items = [
        (0, cfg.get("stars_pieces", False)),      # stars_pieces_1
        (1, cfg.get("stars_pieces", False)),      # stars_pieces_2
        (2, cfg.get("alarm_clocks", False)),
        (3, cfg.get("pleasing_parfait", False)),
        (4, cfg.get("racing_shoes", False)),
        (5, cfg.get("support_points", False)),
        (6, cfg.get("sashes", False)),
    ]

    bought = 0
    on_page2 = False

    for orig_slot, should_buy in all_items:
        if not should_buy:
            continue

        # Position absolue actuelle dans la liste (les achats précédents décalent vers le haut)
        abs_pos = orig_slot - bought

        # Scroll seulement si l'item est encore en page 2 et qu'on n'a pas encore scrollé
        if abs_pos >= 4 and not on_page2:
            time.sleep(1)
            action.tap(*coords("shop_scroll")["tap"])
            time.sleep(0.5)
            action.tap(*coords("shop_scroll")["tap"])
            time.sleep(1)
            on_page2 = True

        if abs_pos <= 3:
            _buy_item(p1_slots_y[abs_pos], p1_x)
        else:
            _buy_item(p2_slots_y[abs_pos - 4], p2_x)

        bought += 1

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
