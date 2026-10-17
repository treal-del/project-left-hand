"""
app.py - Streamlit web app for Project Left Hand.
Run locally with:  streamlit run app.py
"""

import streamlit as st

from logic import (
    ACCESS_ARM, OTHER_ARM, UNSURE,
    EMERGENCY, HIGH, MODERATE,
    DISCLAIMER, assess,
)

st.set_page_config(page_title="Project Left Hand", page_icon="🫀")

st.title("Project Left Hand 🫀")
st.markdown("*Cardiac risk screening for dialysis patients*")
st.info(DISCLAIMER)
st.write("---")

# --- INPUTS ----------------------------------------------------------------
st.header("Patient Information")

bp = st.number_input(
    "Systolic blood pressure (top number, mmHg)",
    min_value=50,
    max_value=250,
    value=120,
)

dialysis = st.checkbox("Is the patient currently on dialysis?")
pain = st.checkbox("Is the patient experiencing arm pain?")

# Only ask which arm when it actually changes the advice.
pain_location = UNSURE
if dialysis and pain:
    choice = st.radio(
        "Where is the arm pain?",
        ["In the arm with the dialysis access",
         "In the other arm",
         "Not sure"],
    )
    pain_location = {
        "In the arm with the dialysis access": ACCESS_ARM,
        "In the other arm": OTHER_ARM,
        "Not sure": UNSURE,
    }[choice]

chest = st.checkbox("Chest pain, shortness of breath, or sweating?")

st.write("---")

# --- OUTPUT ----------------------------------------------------------------
if st.button("Calculate Risk", type="primary"):
    result = assess(
        bp=bp,
        arm_pain=pain,
        dialysis=dialysis,
        chest_symptoms=chest,
        pain_location=pain_location,
    )

    if result.level in (EMERGENCY, HIGH):
        st.error("🔴 " + result.headline)
    elif result.level == MODERATE:
        st.warning("🟡 " + result.headline)
    else:
        st.success("🟢 " + result.headline)

    for line in result.messages:
        st.write("• " + line)

st.write("---")
st.caption(DISCLAIMER)
