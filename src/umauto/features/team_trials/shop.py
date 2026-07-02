"""Buy the configured daily-sale items and return to the trial menu."""

import time

from ... import screen
from ...config import config
from ...driver import driver


def _buy(slot_x, slot_y):
    driver.tap(slot_x, slot_y)
    time.sleep(1.5)
    screen.tap("shop_buy")
    time.sleep(1.5)
    screen.tap("shop_confirm")
    time.sleep(1.5)


def run_shop():
    screen.tap("shop")
    screen.wait("in_shop")

    # Page 1 shows 4 slots; page 2 shows 3 more after scrolling.
    if config.get("steam", False):
        page1_y, page1_x = [467, 594, 734, 847], 764
        page2_y, page2_x = [565, 679, 800], 766
    else:
        page1_y, page1_x = [467, 601, 733, 844], 615
        page2_y, page2_x = [570, 683, 798], 614

    # Item order on the shelf, each paired with its config toggle.
    items = [
        config.get("stars_pieces", False),  # stars_pieces_1
        config.get("stars_pieces", False),  # stars_pieces_2
        config.get("alarm_clocks", False),
        config.get("pleasing_parfait", False),
        config.get("racing_shoes", False),
        config.get("support_points", False),
        config.get("sashes", False),
    ]

    bought = 0
    on_page2 = False
    for original_slot, should_buy in enumerate(items):
        if not should_buy:
            continue

        # Previous purchases shift the remaining items up the list.
        position = original_slot - bought

        if position >= 4 and not on_page2:
            time.sleep(1)
            screen.tap("shop_scroll")
            time.sleep(0.5)
            screen.tap("shop_scroll")
            time.sleep(1)
            on_page2 = True

        if position <= 3:
            _buy(page1_x, page1_y[position])
        else:
            _buy(page2_x, page2_y[position - 4])

        bought += 1

    time.sleep(1)
    screen.tap("shop_close")
    time.sleep(2)
    screen.tap("shop_close_confirm")
    time.sleep(2)
    screen.tap("shop_back")
    screen.wait("tt_button")
    time.sleep(1)
    screen.tap("tt_button")
