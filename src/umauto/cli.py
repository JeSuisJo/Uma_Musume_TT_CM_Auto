"""Interactive menu: choose and launch an automation mode."""

import os

from .driver import StopScript, driver
from .features.registry import FEATURES

_TITLE = "Uma Musume TT CM Auto"
_SEP = "=" * 50


def _render_menu():
    lines = [_SEP, _TITLE, _SEP]
    for key, feature in FEATURES.items():
        lines.append(f"[{key}] {feature.label}")
    lines.append("[0] Exit")
    return "\n".join(lines) + "\n"


def main():
    while True:
        os.system("cls")
        print(_render_menu())
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            return

        feature = FEATURES.get(choice)
        if feature is None:
            continue

        try:
            driver.ensure_ready()
            args = feature.prepare() if feature.prepare else ()
            driver.focus()
            feature.run(*args)
        except StopScript as exc:
            print(f"\n{exc}")
            input("\nPress Enter to return to the menu...")
