import subprocess
import os
import json
import time

ROOT   = os.path.dirname(os.path.abspath(__file__))
ADB    = os.path.join(ROOT, "platform-tools", "adb.exe")
CONFIG = os.path.join(ROOT, "config.json")

if not os.path.exists(ADB):
    print(f"ADB not found: {ADB}")
    input("\nPress Enter to close...")
    exit()

def get_devices():
    r = subprocess.run([ADB, "devices"], capture_output=True, text=True, timeout=10)
    lines = [l for l in r.stdout.strip().split("\n")[1:] if "\tdevice" in l]
    return [l.split("\t")[0] for l in lines]

def save_device(device_id):
    with open(CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)
    config["device_id"] = device_id
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

print("=" * 50)
print("Checking ADB devices...")

devices = get_devices()

if not devices:
    print("No device found. Restarting ADB server...")
    subprocess.run([ADB, "kill-server"], capture_output=True, timeout=10)
    time.sleep(1)
    subprocess.run([ADB, "start-server"], capture_output=True, timeout=15)
    time.sleep(2)
    devices = get_devices()

if devices:
    print(f"\n{len(devices)} device(s) connected:")
    for i, d in enumerate(devices):
        print(f"  [{i+1}] {d}")

    if len(devices) == 1:
        save_device(devices[0])
        print(f"\nDevice ID saved: {devices[0]}")
    else:
        choice = input("\nSelect device to save (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(devices):
            selected = devices[int(choice) - 1]
            save_device(selected)
            print(f"Device ID saved: {selected}")
        else:
            print("No selection made, config.json not changed.")
else:
    print("\nNo device found even after ADB restart.")
    print("Make sure the emulator is running.")

print("=" * 50)
input("\nPress Enter to close...")
