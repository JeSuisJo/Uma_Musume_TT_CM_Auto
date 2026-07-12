# Uma Musume TT/CM Auto

Automation bot for **Team Trials**, **Champions Meeting**, **Daily Races** and **Daily Legends** in Uma Musume Pretty Derby. Supports both **Android (ADB)** and **PC (Steam)**.

## Features

- Automatic Team Trials loop
- Automatic Champions Meeting runs
- Automatic Daily Races (choose reward and difficulty)
- Automatic Daily Legends races (choose the champion)
- **Full Daily routine**: chains Daily Races → Daily Legends → Team Trials in one click
- Difficulty selection (easy / medium / hard)
- Automatic daily shop purchases: buy **everything**, only a **chosen list** of items, or **nothing**
- Automatic parfait usage
- Dual platform support: Android emulator via ADB or Steam PC

## Prerequisites

- **Python 3.10+**
- **Android (ADB)**: an Android emulator (LDPlayer, BlueStacks, etc.)
- **Steam**: the PC version of Uma Musume

### Emulator / Game Settings

| Platform  | Resolution  | Additional |
| --------- | ----------- | ---------- |
| **ADB**   | 1080 x 800  | 240 DPI    |
| **Steam** | 1920 x 1080 | Fullscreen |

### Python Dependencies

Install everything from `pyproject.toml` (recommended):

```bash
pip install -e .
```

Or install the packages by hand:

```bash
pip install pillow opencv-python numpy pyautogui pygetwindow pywin32
```

## Before Starting

You no longer need to be on a specific screen: the bot works from the **Home**
screen **or** the **Race Menu**. Each mode navigates back to Race on its own
before it starts, so either one is fine.

> **Daily Races & Daily Legends:** you must have completed each of these at
> least **once manually** before letting the bot run them. The first manual run
> clears the intro/tutorial screens and unlocks the normal race flow the bot
> relies on. This also applies to the **Full Daily** mode, which chains them.

![Race Menu](img/readme.png)

## Configuration

### `config.json`

| Key                         | Description                                                                      |
| --------------------------- | -------------------------------------------------------------------------------- |
| `steam`                     | `true` for Steam PC mode, `false` for ADB mode                                   |
| `steam_window_title`        | Steam window title (e.g. `"umamusume"`)                                          |
| `device_id`                 | ADB device ID (e.g. `"emulator-5556"`)                                           |
| `difficulty_tm`             | Team Trials difficulty: `"easy"`, `"medium"` or `"hard"`                         |
| `daily_sales_mode`          | Daily shop: `"all"` (buy everything), `"specific"` (buy `shop_items`) or `"off"` |
| `shop_items`                | Item names to buy when `daily_sales_mode` is `"specific"` (see list below)       |
| `use_parfait_TT`            | Use a parfait before each Team Trials run                                        |
| `use_parfait_daily_legends` | Use a parfait before each Daily Legends race                                     |
| `cm_extra_run`              | Do one extra Champions Meeting run                                               |
| `make_your_own_team`        | Use your own CM team instead of the auto-selected one                            |
| `daily_race_difficulty`     | Daily Races difficulty: `"easy"`, `"normal"`, `"hard"` or `"very_hard"`          |
| `daily_race_reward`         | Daily Races reward to farm: `"money"` or `"support"`                             |
| `daily_legends_champion`    | Daily Legends champion to race against (e.g. `"Special Week"`)                   |

When `daily_sales_mode` is `"specific"`, `shop_items` accepts any of:
`"Star Piece"`, `"Alarm Clock"`, `"Pleasing Parfait"`, `"Sprint Shoes"`,
`"Mile Shoes"`, `"Medium Shoes"`, `"Long Shoes"`, `"Dirt Shoes"`,
`"Support Points"`, `"Sash"`.

## Usage

1. Make sure the game is on the **Home** screen or the **Race Menu**
2. Run the bot:

```bash
python main.py
# or, as a package:
python -m umauto
```

On the **first run**, if `config.json` is missing, a short wizard asks for your
platform and preferences and generates it for you. You can also copy
`config.example.json` to `config.json` and edit it by hand.

3. Choose a mode:
   - `[1]` Full Daily (Daily Races + Daily Legends + Team Trials)
   - `[2]` Team Trials
   - `[3]` Champions Meeting
   - `[4]` Daily Races
   - `[5]` Daily Legends Race
   - `[0]` Exit

## Helper Tools

To check connected ADB devices:

```bash
python check_device.py
```

## Project Structure

The code lives in `src/umauto`, laid out **feature-first** (one folder per game
mode) on top of a small shared core. Each file does **one thing**, so a mode
reads as a short list of steps and its `runner.py` just wires them together.

```
src/umauto/
├── app.py            # entry point: run the wizard, then the menu
├── cli.py            # interactive menu that dispatches to a mode
├── config.py         # read-only view over config.json
├── coords.py         # merges coords/*.json into one lookup (per-feature files)
├── screen.py         # semantic screen actions (tap "home", wait "in_shop"...)
├── paths.py          # resolve files relative to the project root
│
├── driver/           # platform backends behind one interface
│   ├── base.py       #   shared image/colour matching
│   ├── adb.py        #   Android emulator (adb)
│   └── steam.py      #   Steam PC window (pyautogui/win32)
│
├── setup/            # first-run config wizard
│   ├── defaults.py   #   default values + option lists
│   ├── prompts.py    #   input() helpers (yes/no, choice, list...)
│   └── wizard.py     #   ask the questions, write config.json
│
├── features/         # one folder per mode, one file per action
│   ├── team_trials/      launch · setup · difficulty · run · finish · runner
│   ├── champions_meeting/ launch · run · reward · team · ticket · runner
│   ├── daily_races/      launch · select · start · race · runner
│   ├── daily_legends/    launch · select · race · champions · runner
│   ├── daily_full/       runner (chains the three dailies)
│   └── shop/             mode · buy_all · buy_specific · dispatch · shop_items
│
└── tools/            # standalone utilities (ADB device check)
```

Adding a mode is a matter of dropping a new `features/<mode>/` folder (action
files + a `runner.py`) and wiring it into `cli.py`.
