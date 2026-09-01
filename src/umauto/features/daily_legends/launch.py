import time

from ... import screen


def open_daily_legends():
    print("Opening the daily program")
    screen.wait_from_home("daily_program_enter")
    screen.tap("daily_program_enter")
    time.sleep(1.5)
    screen.wait("daily_legends_enter")
    screen.tap("daily_legends_enter")
    screen.wait("in_daily_legends")
    time.sleep(0.5)
