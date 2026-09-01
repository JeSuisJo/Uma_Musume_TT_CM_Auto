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
            picked = {int(p) for p in parts}
            return [option for i, option in enumerate(options, 1) if i in picked]
        print(f"  Please enter numbers between 1 and {len(options)}, comma-separated.")
