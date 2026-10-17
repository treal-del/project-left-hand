"""
main.py - command-line version of Project Left Hand.
Run with:  python main.py
"""

from logic import ACCESS_ARM, OTHER_ARM, UNSURE, DISCLAIMER, assess


def ask_yes_no(prompt):
    """Keep asking until the user types yes or no. Returns True or False."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes", "y", "ye"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please enter 'yes' or 'no' (y/n).")


def ask_systolic_bp():
    """Keep asking until the user types a sensible whole number."""
    while True:
        try:
            value = int(input("Systolic blood pressure (top number): "))
        except ValueError:
            print("Please enter a whole number (for example 120).")
            continue
        if 50 <= value <= 250:
            return value
        print("Please enter a value between 50 and 250.")


def ask_pain_location():
    """Ask which arm hurts. Returns ACCESS_ARM, OTHER_ARM or UNSURE."""
    while True:
        answer = input(
            "Is the pain in the arm WITH the dialysis access? "
            "(access / other / unsure): "
        ).strip().lower()
        if answer in ("access", "a"):
            return ACCESS_ARM
        if answer in ("other", "o"):
            return OTHER_ARM
        if answer in ("unsure", "u", "not sure"):
            return UNSURE
        print("Please type access, other, or unsure.")


def main():
    print("=== Project Left Hand: Quick Screening ===")
    print(DISCLAIMER + "\n")

    bp = ask_systolic_bp()
    dialysis = ask_yes_no("Is the patient currently on dialysis? (y/n): ")
    pain = ask_yes_no("Is the patient experiencing arm pain? (y/n): ")

    pain_location = UNSURE
    if dialysis and pain:
        pain_location = ask_pain_location()

    chest = ask_yes_no(
        "Chest pain, shortness of breath, or sweating? (y/n): "
    )

    result = assess(
        bp=bp,
        arm_pain=pain,
        dialysis=dialysis,
        chest_symptoms=chest,
        pain_location=pain_location,
    )

    print("\n=== Result ===")
    print(result.headline)
    for line in result.messages:
        print(" - " + line)


if __name__ == "__main__":
    main()
