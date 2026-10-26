"""Safety-focused educational guidance for Project Left Hand.

This module intentionally does NOT calculate or estimate cardiac risk. It
surfaces selected warning signs and encourages appropriate human care. It is
not a diagnostic device, a validated screening instrument, or a substitute for
emergency services or a clinician's advice.
"""

from dataclasses import dataclass
from math import isfinite
from typing import Optional

# Guidance urgency labels describe the action presented, not a disease risk.
EMERGENCY = "emergency"
PROMPT_CARE = "prompt_care"
INFORMATION_ONLY = "information_only"

ACCESS_FISTULA = "fistula"
ACCESS_GRAFT = "graft"
ACCESS_CATHETER = "catheter"
ACCESS_UNSURE = "unsure"
ACCESS_TYPES = {ACCESS_FISTULA, ACCESS_GRAFT, ACCESS_CATHETER, ACCESS_UNSURE}

DISCLAIMER = (
    "EDUCATIONAL AWARENESS TOOL ONLY — NOT MEDICAL ADVICE, NOT A DIAGNOSIS, "
    "AND NOT A VALIDATED SCREENING TOOL. It cannot rule out a heart problem. "
    "If a medical emergency may be happening, call your local emergency number "
    "now; do not wait for this checklist."
)

NSAID_REMINDER = (
    "If you receive dialysis, ask your nephrology/dialysis team before using "
    "over-the-counter pain medicines such as ibuprofen or naproxen. Do not "
    "start, stop, or change a prescribed medicine based on this tool."
)

EMERGENCY_MESSAGE = (
    "The symptoms selected can be warning signs of a medical emergency. Call "
    "your local emergency number now. Do not wait for this tool to finish and "
    "do not drive yourself. Tell the dispatcher about the symptoms and whether "
    "the person receives dialysis. This tool cannot determine the cause."
)


@dataclass(frozen=True)
class Guidance:
    """Action guidance; status is not a clinical risk category."""

    status: str
    headline: str
    messages: tuple[str, ...]
    emergency: bool = False


def _validate_optional_pressure(name: str, value: Optional[float]) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a positive number or None.")
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number or None.")


def _validate_bool(name: str, value: bool) -> None:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be True or False.")


def assess(
    *,
    systolic_bp: Optional[float] = None,
    diastolic_bp: Optional[float] = None,
    dialysis: bool = False,
    chest_discomfort: bool = False,
    shortness_of_breath: bool = False,
    unexplained_upper_body_pain: bool = False,
    cold_sweat_nausea_or_lightheadedness: bool = False,
    sudden_neurologic_symptoms: bool = False,
    fainting_or_severe_weakness: bool = False,
    feeling_severely_unwell: bool = False,
    access_type: str = ACCESS_UNSURE,
    access_site_changes: bool = False,
    access_vibration_changed: bool = False,
    catheter_or_dressing_problem: bool = False,
    fever_or_chills: bool = False,
    access_bleeding_uncontrolled: bool = False,
) -> Guidance:
    """Return conservative, non-diagnostic safety guidance.

    Blood pressure values are optional context. They never produce a cardiac
    risk score. Symptoms suggesting a possible acute emergency take priority.
    Access-specific checks are displayed only as general prompts to contact a
    dialysis team; they are not interpreted as diagnoses.
    """
    _validate_optional_pressure("Systolic blood pressure", systolic_bp)
    _validate_optional_pressure("Diastolic blood pressure", diastolic_bp)
    bool_fields = {
        "dialysis": dialysis,
        "chest_discomfort": chest_discomfort,
        "shortness_of_breath": shortness_of_breath,
        "unexplained_upper_body_pain": unexplained_upper_body_pain,
        "cold_sweat_nausea_or_lightheadedness": cold_sweat_nausea_or_lightheadedness,
        "sudden_neurologic_symptoms": sudden_neurologic_symptoms,
        "fainting_or_severe_weakness": fainting_or_severe_weakness,
        "feeling_severely_unwell": feeling_severely_unwell,
        "access_site_changes": access_site_changes,
        "access_vibration_changed": access_vibration_changed,
        "catheter_or_dressing_problem": catheter_or_dressing_problem,
        "fever_or_chills": fever_or_chills,
        "access_bleeding_uncontrolled": access_bleeding_uncontrolled,
    }
    for name, value in bool_fields.items():
        _validate_bool(name, value)
    if not isinstance(access_type, str) or access_type not in ACCESS_TYPES:
        raise ValueError(f"access_type must be one of {sorted(ACCESS_TYPES)}.")

    messages: list[str] = []
    emergency_symptoms = any((
        chest_discomfort,
        shortness_of_breath,
        unexplained_upper_body_pain,
        cold_sweat_nausea_or_lightheadedness,
        sudden_neurologic_symptoms,
        fainting_or_severe_weakness,
        feeling_severely_unwell,
        access_bleeding_uncontrolled,
    ))

    # An emergency warning always wins; no lower-priority rule may mask it.
    if emergency_symptoms:
        messages.append(EMERGENCY_MESSAGE)
        if access_bleeding_uncontrolled:
            messages.append(
                "For heavy or uncontrolled bleeding from dialysis access, call "
                "emergency services. Apply firm, steady pressure with clean "
                "gauze or a clean cloth while help is being arranged."
            )
        if dialysis and any((
            access_site_changes, access_vibration_changed,
            catheter_or_dressing_problem, fever_or_chills,
        )):
            messages.append(
                "Also tell the emergency dispatcher about the dialysis access "
                "changes. Do not delay emergency help to contact the dialysis unit."
            )
        if dialysis:
            messages.append(NSAID_REMINDER)
        return Guidance(EMERGENCY, "Emergency symptoms selected", tuple(messages), True)

    # Severe readings trigger prompt clinician contact, but a number alone is
    # not labelled a hypertensive emergency and does not produce a risk score.
    very_high_bp = (
        (systolic_bp is not None and systolic_bp > 180)
        or (diastolic_bp is not None and diastolic_bp > 120)
    )
    low_systolic = systolic_bp is not None and systolic_bp < 90

    if very_high_bp:
        messages.append(
            "This reading is in a very high range. If it is safe to do so, sit "
            "quietly and repeat the measurement after at least one minute. If "
            "the reading remains this high, contact a healthcare professional "
            "immediately for instructions. If chest discomfort, trouble "
            "breathing, weakness/numbness, vision changes, trouble speaking, "
            "or another severe/new symptom occurs, call emergency services now. "
            "Do not change medicine doses based on this tool."
        )

    if low_systolic:
        messages.append(
            "The systolic reading is below 90 mm Hg. This can be concerning, "
            "especially during or after dialysis. Contact the person's clinician "
            "or dialysis team promptly for advice. If there is fainting, severe "
            "weakness, confusion, chest discomfort, or trouble breathing, call "
            "emergency services now."
        )

    access_concern = dialysis and any((
        access_site_changes, fever_or_chills,
        # Thrill/vibration is relevant to a fistula or graft, not a catheter.
        (access_vibration_changed and access_type in (ACCESS_FISTULA, ACCESS_GRAFT, ACCESS_UNSURE)),
        # Dressing/line problems are relevant to a catheter or unknown access.
        (catheter_or_dressing_problem and access_type in (ACCESS_CATHETER, ACCESS_UNSURE)),
    ))
    if access_concern:
        messages.append(
            "Contact the dialysis team or treating clinician now for advice "
            "about the access change, pain, skin changes, fever/chills, or "
            "catheter/dressing problem. Do not wait until the next routine "
            "dialysis visit. Follow the access-care instructions your team gave you."
        )

    needs_prompt_care = very_high_bp or low_systolic or access_concern
    if dialysis:
        messages.append(NSAID_REMINDER)

    if needs_prompt_care:
        return Guidance(
            PROMPT_CARE,
            "Contact a healthcare professional for guidance",
            tuple(messages),
            False,
        )

    return Guidance(
        INFORMATION_ONLY,
        "This checklist cannot assess or rule out a heart problem",
        (
            "No emergency warning item was selected, but that does not mean a "
            "person is low risk or medically safe. This tool does not estimate "
            "cardiac risk and cannot rule out a heart problem. Follow the person's "
            "care plan and contact their healthcare team if you are concerned.",
        ) + ((NSAID_REMINDER,) if dialysis else ()),
        False,
    )
