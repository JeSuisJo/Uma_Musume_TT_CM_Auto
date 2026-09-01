import importlib.util
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SRC = _ROOT / "src" / "umauto"
_COORDS_DIR = _ROOT / "coords"


def _load(relative_path):
    path = _SRC / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_defaults = _load("setup/defaults.py")
_shop_items = _load("features/shop/shop_items.py")
_champions = _load("features/daily_legends/champions.py")


def test_shop_items_match_wizard_defaults():
    assert _shop_items.NAMES == _defaults.SHOP_ITEMS


def test_daily_champions_match_wizard_defaults():
    assert _champions.NAMES == _defaults.DAILY_CHAMPIONS


def _coord_files():
    return sorted(_COORDS_DIR.glob("*.json"))


def test_coords_have_no_duplicate_names():
    seen = {}
    for path in _coord_files():
        for name in json.loads(path.read_text(encoding="utf-8")):
            assert name not in seen, (
                f"coord '{name}' defined in both {seen[name]} and {path.name}"
            )
            seen[name] = path.name


def test_every_referenced_template_image_exists():
    missing = []
    for path in _coord_files():
        entries = json.loads(path.read_text(encoding="utf-8"))
        for name, block in entries.items():
            for platform, spec in block.items():
                img = spec.get("img")
                if img and not (_ROOT / img).exists():
                    missing.append(f"{name} [{platform}] -> {img} ({path.name})")
    assert not missing, "Missing template images:\n  " + "\n  ".join(missing)


if __name__ == "__main__":
    test_shop_items_match_wizard_defaults()
    test_daily_champions_match_wizard_defaults()
    test_coords_have_no_duplicate_names()
    test_every_referenced_template_image_exists()
    print("OK: wizard defaults synced, coords unique, all template images present")
