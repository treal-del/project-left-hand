import streamlit as st

# Title of the web page
st.title("Project Left Hand 🫀")
st.markdown("*Cardiac risk screening for dialysis patients*")

st.write("---")  # Draws a horizontal line

# INPUT SECTION
st.header("Patient Information")

# Number input for blood pressure
bp = st.number_input(
    "Systolic Blood Pressure (top number)", 
    min_value=50, 
    max_value=250, 
    value=120
)

# Checkboxes for symptoms
pain = st.checkbox("Is the patient experiencing arm pain?")
dialysis = st.checkbox("Is the patient currently on dialysis?")

st.write("---")

# BUTTON AND OUTPUT
if st.button("Calculate Risk", type="primary"):
    
    # EMERGENCY first
    if bp >= 180:
        st.error("🔴 EMERGENCY: Hypertensive Crisis (BP ≥ 180). Seek immediate care.")
    elif bp < 90:
        st.error("🔴 EMERGENCY: Hypotension (BP < 90). Seek immediate care.")
    
    # HIGH RISK
    elif bp >= 140 and (pain or dialysis):
        st.error("🔴 HIGH RISK: See a cardiologist today.")
        if dialysis and pain:
            st.warning("⚠️ Check vascular access site immediately.")
    
    # MODERATE RISK
    elif bp >= 140 or dialysis:
        st.warning("🟡 MODERATE RISK: Monitor closely and schedule follow-up.")
    
    # LOW RISK
    else:
        st.success("🟢 LOW RISK: Continue routine monitoring.")
    
    # NSAID warning for all dialysis patients
    if dialysis:
        st.info("💊 Reminder: Dialysis patients must not take NSAIDs (like ibuprofen) without nephrologist approval.")