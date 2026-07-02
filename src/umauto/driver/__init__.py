"""Active driver instance, selected from config.

The concrete backend is imported lazily so an ADB-only machine never needs the
Steam dependencies (pywin32, pyautogui) and vice versa.
"""

from ..config import config
from .base import Driver, StopScript


def create_driver():
    """Build the driver matching the configured platform."""
    if config.get("steam", False):
        from .steam import SteamDriver

        return SteamDriver()

    from .adb import AdbDriver

    return AdbDriver()


driver = create_driver()

__all__ = ["Driver", "StopScript", "create_driver", "driver"]
