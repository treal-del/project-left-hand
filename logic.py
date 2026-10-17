"""
logic.py - the single source of truth for Project Left Hand's risk rules.

Both the web app (app.py) and the command-line tool (main.py) call assess(),
so a fix made here applies to both.

EDUCATIONAL TOOL ONLY. It does not diagnose anything and is not a substitute
for a doctor or emergency services.
"""

from dataclasses import dataclass, field

# --- Risk levels -----------------------------------------------------------
EMERGENCY = "emergency"
HIGH = "high"
MODERATE = "moderate"
LOW = "low"

# --- Where the arm pain is (only matters for dialysis patients) ------------
ACCESS_ARM = "access_arm"   # the arm with the fistula / graft / catheter
OTHER_ARM = "other_arm"     # the arm without the dialysis access
UNSURE = "unsure"

DISCLAIMER = (
    "This tool does not diagnose any condition and is not medical advice. "
    "If someone has chest pain, trouble breathing, or feels very unwell, "
    "call your local emergency number immediately."
)

NSAID_REMINDER = (
    "Dialysis patients must not take NSAIDs (like ibuprofen) "
    "without nephrologist approval."
)


@dataclass
class Assessment:
    level: str                       # one of EMERGENCY, HIGH, MODERATE, LOW
    headline: str                    # short title for the result
    messages: list = field(default_factory=list)  # advice lines, in order


def assess(bp, arm_pain, dialysis, chest_symptoms=False, pain_location=UNSURE):
    """
    Work out a risk level from a few simple inputs.

    bp              -- systolic blood pressure (top number), in mmHg
    arm_pain        -- True if the patient has arm pain
    dialysis        -- True if the patient is currently on dialysis
    chest_symptoms  -- True for chest pain, shortness of breath, or sweating
    pain_location   -- ACCESS_ARM, OTHER_ARM or UNSURE (used only when the
                       patient is on dialysis AND has arm pain)
    """
    if bp <= 0:
        raise ValueError("Blood pressure must be a positive number.")

    # Advice that applies at EVERY risk level goes in first, so it can never
    # be skipped by an earlier branch (this was the original app.py bug).
    notes = []

    if dialysis and arm_pain:
        if pain_location in (ACCESS_ARM, UNSURE):
            notes.append(
                "Check the vascular access site now for swelling, redness, "
                "warmth, or a weak or missing thrill/pulse, and tell the "
                "dialysis team."
            )
        if pain_location in (OTHER_ARM, UNSURE):
            notes.append(
                "Arm pain away from the access site (especially the left arm) "
                "can be a sign of a heart problem in dialysis patients, "
                "so it should not be ignored."
            )

    if dialysis:
        notes.append(NSAID_REMINDER)

    # --- Emergencies come first -------------------------------------------
    if chest_symptoms:
        return Assessment(
            EMERGENCY,
            "EMERGENCY: chest symptoms reported",
            ["Chest pain, breathlessness, or sweating can signal a heart "
             "attack. Call emergency services now."] + notes,
        )

    if bp > 180:
        return Assessment(
            EMERGENCY,
            "EMERGENCY: hypertensive crisis (systolic above 180)",
            ["Seek emergency medical care immediately."] + notes,
        )

    if bp < 90:
        if dialysis:
            first = ("Low blood pressure during or after dialysis can cause "
                     "dizziness and cramps. Tell the dialysis nursing staff "
                     "or a doctor immediately.")
        else:
            first = ("Sit or lie down safely to avoid fainting and contact "
                     "a doctor right away.")
        return Assessment(
            EMERGENCY,
            "EMERGENCY: low blood pressure (systolic below 90)",
            [first] + notes,
        )

    # --- Non-emergency levels ---------------------------------------------
    pain_away_from_access = (
        dialysis and arm_pain and pain_location in (OTHER_ARM, UNSURE)
    )

    if (bp >= 140 and (arm_pain or dialysis)) or pain_away_from_access:
        return Assessment(
            HIGH,
            "HIGH RISK: see a cardiologist or doctor today",
            ["Do not wait for the next routine appointment."] + notes,
        )

    if bp >= 140 or dialysis or arm_pain:
        return Assessment(
            MODERATE,
            "MODERATE RISK: monitor closely",
            ["Keep watching symptoms and schedule a follow-up. If the pain "
             "gets worse, spreads, or comes with chest symptoms, treat it as "
             "an emergency."] + notes,
        )

    return Assessment(
        LOW,
        "LOW RISK: continue routine monitoring",
        ["No warning signs from the information entered."] + notes,
    )
