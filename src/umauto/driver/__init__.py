from ..config import config
from .base import Driver, StopScript


def create_driver():
    if config.get("steam", False):
        from .steam import SteamDriver

        return SteamDriver()

    from .adb import AdbDriver

    return AdbDriver()


driver = create_driver()

__all__ = ["Driver", "StopScript", "create_driver", "driver"]
