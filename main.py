"""Command-line interface for Project Left Hand's educational guidance tool."""

from math import isfinite

from logic import (
    ACCESS_CATHETER, ACCESS_FISTULA, ACCESS_GRAFT, ACCESS_UNSURE,
    DISCLAIMER, EMERGENCY, PROMPT_CARE, assess,
)


def ask_yes_no(prompt: str) -> bool:
    """Keep asking until the user gives a yes/no answer."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please enter yes or no (y/n).")


def ask_optional_number(prompt: str):
    """Return an optional positive reading; blank or 0 means unknown."""
    while True:
        answer = input(prompt).strip()
        if answer == "" or answer == "0":
            return None
        try:
            value = float(answer)
        except ValueError:
            print("Please enter a number, 0, or press Enter if unknown.")
            continue
        if isfinite(value) and value > 0:
            return value
        print("Enter a positive number, 0, or press Enter if unknown.")


def ask_access_type() -> str:
    while True:
        answer = input("Access type (fistula/graft/catheter/unsure): ").strip().lower()
        choices = {
            "fistula": ACCESS_FISTULA, "f": ACCESS_FISTULA,
            "graft": ACCESS_GRAFT, "g": ACCESS_GRAFT,
            "catheter": ACCESS_CATHETER, "c": ACCESS_CATHETER,
            "unsure": ACCESS_UNSURE, "u": ACCESS_UNSURE,
        }
        if answer in choices:
            return choices[answer]
        print("Please enter fistula, graft, catheter, or unsure.")


def main() -> None:
    print("=== Project Left Hand: Educational Awareness Checklist ===")
    print(DISCLAIMER + "\n")
    print("If emergency symptoms are happening now, call your local emergency number now.\n")

    have_bp = ask_yes_no("Do you have a recent blood-pressure reading? (y/n): ")
    systolic = ask_optional_number("Systolic/top number (0 or Enter if unknown): ") if have_bp else None
    diastolic = ask_optional_number("Diastolic/bottom number (0 or Enter if unknown): ") if have_bp else None

    dialysis = ask_yes_no("Does the person receive dialysis? (y/n): ")
    chest = ask_yes_no("Chest pain/pressure/discomfort? (y/n): ")
    breathless = ask_yes_no("Shortness of breath or difficulty breathing? (y/n): ")
    upper_body = ask_yes_no(
        "New/unexplained discomfort in an arm, back, neck, jaw, or stomach? (y/n): "
    )
    sweat_nausea = ask_yes_no("Cold sweat, nausea, or lightheadedness with concern about a heart problem? (y/n): ")
    neuro = ask_yes_no("Sudden weakness/numbness, vision change, or trouble speaking? (y/n): ")
    fainting = ask_yes_no("Fainting or severe weakness? (y/n): ")
    very_unwell = ask_yes_no("Does the person feel severely or suddenly unwell? (y/n): ")

    access_type = ACCESS_UNSURE
    access_site = vibration = catheter_issue = fever = bleeding = False
    if dialysis:
        access_type = ask_access_type()
        access_site = ask_yes_no("Redness, warmth, swelling, pain, or drainage near access? (y/n): ")
        if access_type in (ACCESS_FISTULA, ACCESS_GRAFT, ACCESS_UNSURE):
            vibration = ask_yes_no("If fistula/graft: usual access vibration has stopped or changed? (y/n): ")
        if access_type in (ACCESS_CATHETER, ACCESS_UNSURE):
            catheter_issue = ask_yes_no("If catheter: line/dressing loose, wet, dirty, damaged, or displaced? (y/n): ")
        fever = ask_yes_no("Fever or chills? (y/n): ")
        bleeding = ask_yes_no("Heavy access bleeding, or bleeding that will not stop? (y/n): ")

    result = assess(
        systolic_bp=systolic, diastolic_bp=diastolic, dialysis=dialysis,
        chest_discomfort=chest, shortness_of_breath=breathless,
        unexplained_upper_body_pain=upper_body,
        cold_sweat_nausea_or_lightheadedness=sweat_nausea,
        sudden_neurologic_symptoms=neuro,
        fainting_or_severe_weakness=fainting,
        feeling_severely_unwell=very_unwell,
        access_type=access_type, access_site_changes=access_site,
        access_vibration_changed=vibration,
        catheter_or_dressing_problem=catheter_issue,
        fever_or_chills=fever, access_bleeding_uncontrolled=bleeding,
    )
    print("\n=== Safety guidance (not a diagnosis) ===")
    print(result.headline)
    for message in result.messages:
        print("- " + message)
    if result.status not in (EMERGENCY, PROMPT_CARE):
        print("Reminder: this checklist cannot rule out a heart problem.")


if __name__ == "__main__":
    main()
