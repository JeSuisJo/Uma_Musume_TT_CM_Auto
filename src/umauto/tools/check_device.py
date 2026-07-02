"""Detect connected ADB devices and save the chosen one to config.json."""

import json
import os
import subprocess
import time

from ..paths import resolve

_ADB = resolve("platform-tools/adb.exe")
_CONFIG = resolve("config.json")


def _list_devices():
    result = subprocess.run(
        [_ADB, "devices"], capture_output=True, text=True, timeout=10
    )
    lines = [
        line for line in result.stdout.strip().split("\n")[1:] if "\tdevice" in line
    ]
    return [line.split("\t")[0] for line in lines]


def _save_device(device_id):
    with open(_CONFIG, encoding="utf-8") as f:
        data = json.load(f)
    data["device_id"] = device_id
    with open(_CONFIG, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    if not os.path.exists(_ADB):
        print(f"ADB not found: {_ADB}")
        input("\nPress Enter to close...")
        return

    print("=" * 50)
    print("Checking ADB devices...")

    devices = _list_devices()
    if not devices:
        print("No device found. Restarting ADB server...")
        subprocess.run([_ADB, "kill-server"], capture_output=True, timeout=10)
        time.sleep(1)
        subprocess.run([_ADB, "start-server"], capture_output=True, timeout=15)
        time.sleep(2)
        devices = _list_devices()

    if not devices:
        print("\nNo device found even after ADB restart.")
        print("Make sure the emulator is running.")
    elif len(devices) == 1:
        _save_device(devices[0])
        print(f"\nDevice ID saved: {devices[0]}")
    else:
        print(f"\n{len(devices)} device(s) connected:")
        for i, device in enumerate(devices, 1):
            print(f"  [{i}] {device}")
        choice = input("\nSelect device to save (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(devices):
            selected = devices[int(choice) - 1]
            _save_device(selected)
            print(f"Device ID saved: {selected}")
        else:
            print("No selection made, config.json not changed.")

    print("=" * 50)
    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()
