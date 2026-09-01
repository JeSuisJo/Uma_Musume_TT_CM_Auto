import glob
import json
import os

from .config import config
from .paths import resolve

_MODE = "steam" if config.get("steam", False) else "adb"

_COORDS_DIR = resolve("coords")


def _load():
    merged = {}
    origin = {}
    for path in sorted(glob.glob(os.path.join(_COORDS_DIR, "*.json"))):
        name_of_file = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            entries = json.load(f)
        for name, block in entries.items():
            if name in merged:
                raise ValueError(
                    f"Duplicate coord '{name}' defined in both "
                    f"'{origin[name]}' and '{name_of_file}'"
                )
            merged[name] = block
            origin[name] = name_of_file
    return merged


_COORDS = _load()


def coords(name):
    return _COORDS[name][_MODE]
