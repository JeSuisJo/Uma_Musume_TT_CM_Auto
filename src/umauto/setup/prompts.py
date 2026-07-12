"""Interactive prompt helpers for the first-run wizard.

Pure ``input()`` wrappers, one per answer shape (yes/no, free text, fixed
choice, pick-one-from-list, pick-many-from-list). They keep no state and import
nothing, so the wizard flow reads as a list of questions.
"""


def ask_bool(prompt, default):
    suffix = "[Y/n]" if default else "[y/N]"
    truthy = {"y", "yes", "o", "oui"}
    falsy = {"n", "no", "non"}
    while True:
        answer = input(f"{prompt} {suffix} ").strip().lower()
        if not answer:
            return default
        if answer in truthy:
            return True
        if answer in falsy:
            return False
        print("  Please answer y or n.")


def ask_str(prompt, default):
    answer = input(f"{prompt} [{default}] ").strip()
    return answer or default


def ask_choice(prompt, options, default):
    joined = "/".join(options)
    while True:
        answer = input(f"{prompt} ({joined}) [{default}] ").strip().lower()
        if not answer:
            return default
        if answer in options:
            return answer
        print(f"  Please choose one of: {joined}.")


def ask_from_list(prompt, options, default):
    default_index = options.index(default) + 1 if default in options else 1
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"  [{i}] {option}")
        answer = input(f"Choice [{default_index}]: ").strip()
        if not answer:
            return options[default_index - 1]
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        print(f"  Please enter a number between 1 and {len(options)}.")


def ask_multi_from_list(prompt, options, default):
    """Ask for zero or more picks from a list (comma-separated numbers).

    Returns the chosen display names in list order. An empty answer keeps
    ``default``; "all" selects everything.
    """
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"  [{i}] {option}")
        answer = input("Choices (e.g. 1,3 or 'all') []: ").strip().lower()
        if not answer:
            return list(default)
        if answer == "all":
            return list(options)
        parts = [p.strip() for p in answer.split(",") if p.strip()]
        if all(p.isdigit() and 1 <= int(p) <= len(options) for p in parts):
            # De-duplicate while keeping the list's display order.
            picked = {int(p) for p in parts}
            return [option for i, option in enumerate(options, 1) if i in picked]
        print(f"  Please enter numbers between 1 and {len(options)}, comma-separated.")
