# Uma Musume TT/CM Auto

Automation bot for **Team Trials** and **Champions Meeting** in Uma Musume Pretty Derby. Supports both **Android (ADB)** and **PC (Steam)**.

## Features

- Automatic Team Trials loop
- Difficulty selection (easy / medium / hard)
- Automatic daily shop purchases (configurable per item)
- Automatic parfait usage
- Dual platform support: Android emulator via ADB or Steam PC

## Prerequisites

- **Python 3.10+**
- **Android (ADB)**: an Android emulator (LDPlayer, BlueStacks, etc.)
- **Steam**: the PC version of Uma Musume

### Emulator / Game Settings

| Platform | Resolution | Additional |
|----------|-----------|------------|
| **ADB** | 1080 x 800 | 240 DPI |
| **Steam** | 1920 x 1080 | Fullscreen |

### Python Dependencies

```bash
pip install Pillow pyautogui pygetwindow matplotlib
```

## Before Starting

Make sure the game is on the **Race Menu** screen before launching the bot:

![Race Menu](readme.png)

## Configuration

### `config.json`

| Key | Type | Description |
|-----|------|-------------|
| `steam` | bool | `true` for Steam PC mode, `false` for ADB mode |
| `steam_window_title` | string | Steam window title (e.g. `"umamusume"`) |
| `device_id` | string | ADB device ID (e.g. `"emulator-5556"`) |
| `difficulty_tm` | string | Team Trials difficulty: `"easy"`, `"medium"` or `"hard"` |
| `daily_sales_buy` | bool | Auto-buy from the daily shop |
| `alarm_clocks` | bool | Buy alarm clocks |
| `stars_pieces` | bool | Buy star pieces |
| `pleasing_parfait` | bool | Buy pleasing parfaits |
| `support_points` | bool | Buy support points |
| `racing_shoes` | bool | Buy racing shoes |
| `sashes` | bool | Buy sashes |
| `use_rp` | bool | Use RP (not implemented yet)|
| `use_parfait` | bool | Use a parfait before each run |

## Usage

1. Set up `config.json` with your platform and preferences
2. Make sure the game is on the **Race Menu** (see screenshot above)
3. Run the bot:

```bash
python main.py
```

4. Choose a mode:
   - `[1]` Team Trials
   - `[2]` Champions Meeting
   - `[0]` Exit

## Helper Tools
To check connected ADB devices:

```bash
python check_id.py
```
