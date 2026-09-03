import time

from .. import screen


def dismiss_uma_outing():
    if not screen.see("next_uma_outing"):
        return False

    print("Dismissing the uma outing popup")
    time.sleep(0.5)
    screen.tap("next_uma_outing")
    time.sleep(2.5)
    return True
