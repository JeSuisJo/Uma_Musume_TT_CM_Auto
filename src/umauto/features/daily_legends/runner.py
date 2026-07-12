"""Daily Legends Race mode: run a single race with the configured champion."""

import os

from ...config import config
from .champions import DEFAULT
from .launch import open_daily_legends
from .race import run_race
from .select import select_champion


def run():
    os.system("cls")
    print("=" * 50)
    print("Uma Musume Daily Legends Race Auto")
    print("=" * 50)

    champion = config.get("daily_legends_champion", DEFAULT)

    open_daily_legends()
    select_champion(champion)
    run_race()

    print("Daily legends race finished")
