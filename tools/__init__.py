import os
import json

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(_root, "config.json"), encoding="utf-8") as f:
    _cfg = json.load(f)

_use_steam = _cfg.get("steam", False)
_mode = "steam" if _use_steam else "adb"

with open(os.path.join(_root, "coords.json"), encoding="utf-8") as f:
    _coords_all = json.load(f)

def coords(name):
    return _coords_all[name][_mode]

if _use_steam:
    from .steam import (
        path, StopScriptException,
        tap, hold, swipe, write, enter, delete, stop,
        compare_image, wait_for_image,
        get_color, is_color, wait_for_color,
        _screenshot,
    )
else:
    from .adb import (
        path, StopScriptException,
        tap, hold, swipe, write, enter, delete, stop,
        compare_image, wait_for_image,
        get_color, is_color, wait_for_color,
        _screenshot,
    )
