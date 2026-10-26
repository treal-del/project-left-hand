"""Streamlit interface for Project Left Hand's educational guidance tool."""

import streamlit as st

from logic import (
    ACCESS_CATHETER, ACCESS_FISTULA, ACCESS_GRAFT, ACCESS_UNSURE,
    EMERGENCY, PROMPT_CARE, DISCLAIMER, assess,
)

st.set_page_config(page_title="Project Left Hand", page_icon="🫀", layout="centered")
st.title("Project Left Hand 🫀")
st.subheader("Cardiac and dialysis-access awareness")
st.error(
    "If someone may be having a medical emergency, call your local emergency "
    "number now. Do not wait to complete this checklist."
)
st.info(DISCLAIMER)
st.markdown(
    "This educational checklist highlights selected warning signs. It does "
    "**not** calculate cardiac risk, diagnose a condition, or prove that a "
    "person is safe. The same symptoms can have different causes."
)

st.header("1. Symptoms happening now")
st.caption(
    "Select any items that are happening now. If a severe/new symptom is "
    "present, use emergency services rather than relying on this page."
)
chest = st.checkbox("Chest pain, pressure, tightness, or discomfort")
breathless = st.checkbox("Shortness of breath or difficulty breathing")
upper_body = st.checkbox(
    "New or unexplained discomfort in an arm, back, neck, jaw, or stomach"
)
sweat_nausea = st.checkbox("Cold sweat, nausea, or lightheadedness with concern about a heart problem")
neuro = st.checkbox("Sudden weakness or numbness, vision change, or trouble speaking")
fainting = st.checkbox("Fainting or severe weakness")
very_unwell = st.checkbox("The person feels severely or suddenly unwell")

st.header("2. Optional blood-pressure reading")
have_bp = st.checkbox("I have a recent blood-pressure reading")
systolic = None
diastolic = None
if have_bp:
    col1, col2 = st.columns(2)
    with col1:
        sys_value = st.number_input(
            "Systolic (top number, mmHg; 0 = unknown)",
            min_value=0, max_value=300, value=0, step=1,
        )
    with col2:
        dia_value = st.number_input(
            "Diastolic (bottom number, mmHg; 0 = unknown)",
            min_value=0, max_value=200, value=0, step=1,
        )
    systolic = int(sys_value) if sys_value else None
    diastolic = int(dia_value) if dia_value else None
    if systolic is None and diastolic is None:
        st.caption("Enter the values you have; keep 0 for a number you do not know.")

st.header("3. Dialysis and access concerns")
dialysis = st.checkbox("The person receives dialysis")
access_type = ACCESS_UNSURE
access_site_changes = False
access_vibration_changed = False
catheter_issue = False
fever_or_chills = False
access_bleeding = False
if dialysis:
    access_choice = st.selectbox(
        "Dialysis access type (if known)",
        options=["Not sure", "Fistula", "Graft", "Catheter"],
        help="Ask the dialysis team if you do not know the access type.",
    )
    access_type = {
        "Not sure": ACCESS_UNSURE,
        "Fistula": ACCESS_FISTULA,
        "Graft": ACCESS_GRAFT,
        "Catheter": ACCESS_CATHETER,
    }[access_choice]
    access_site_changes = st.checkbox(
        "Redness, warmth, swelling, pain, or drainage near the access"
    )
    if access_type in (ACCESS_FISTULA, ACCESS_GRAFT, ACCESS_UNSURE):
        access_vibration_changed = st.checkbox(
            "If a fistula/graft is present: its usual buzzing/vibration has stopped or changed"
        )
    if access_type in (ACCESS_CATHETER, ACCESS_UNSURE):
        catheter_issue = st.checkbox(
            "If a catheter is present: its line/dressing is loose, wet, dirty, damaged, or displaced"
        )
    fever_or_chills = st.checkbox("Fever or chills")
    access_bleeding = st.checkbox("Heavy bleeding from the dialysis access, or bleeding that will not stop")
    st.caption(
        "Access care differs by access type. Follow instructions from the person's "
        "dialysis team; do not open, adjust, or remove a catheter yourself."
    )

potential_emergency_selected = any((
    chest, breathless, upper_body, sweat_nausea, neuro, fainting,
    very_unwell, access_bleeding,
))
if potential_emergency_selected:
    st.error(
        "You selected a potential emergency warning sign. Call your local "
        "emergency number now; do not wait to submit this checklist."
    )

st.write("---")
if st.button("Show safety guidance", type="primary", use_container_width=True):
    result = assess(
        systolic_bp=systolic,
        diastolic_bp=diastolic,
        dialysis=dialysis,
        chest_discomfort=chest,
        shortness_of_breath=breathless,
        unexplained_upper_body_pain=upper_body,
        cold_sweat_nausea_or_lightheadedness=sweat_nausea,
        sudden_neurologic_symptoms=neuro,
        fainting_or_severe_weakness=fainting,
        feeling_severely_unwell=very_unwell,
        access_type=access_type,
        access_site_changes=access_site_changes,
        access_vibration_changed=access_vibration_changed,
        catheter_or_dressing_problem=catheter_issue,
        fever_or_chills=fever_or_chills,
        access_bleeding_uncontrolled=access_bleeding,
    )
    if result.status == EMERGENCY:
        st.error("🚨 " + result.headline)
    elif result.status == PROMPT_CARE:
        st.warning("⚠️ " + result.headline)
    else:
        # Never show a green success state or a “low risk” label.
        st.info("ℹ️ " + result.headline)
    for message in result.messages:
        st.write("- " + message)
    st.caption("This output is general educational guidance, not a clinical assessment.")

st.write("---")
st.subheader("Educational references")
st.markdown(
    "- [American Heart Association: warning signs of a heart attack](https://www.heart.org/en/health-topics/heart-attack/warning-signs-of-a-heart-attack)\n"
    "- [American Heart Association: understanding blood-pressure readings](https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings)\n"
    "- [National Kidney Foundation: hemodialysis access care](https://www.kidney.org/kidney-topics/hemodialysis-access)"
)
st.caption(DISCLAIMER)
