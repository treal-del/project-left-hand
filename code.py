def ask_yes_no(prompt):
    """Safely collects a yes or no input and returns a boolean."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ['yes', 'y', 'ye']:
            return True
        elif answer in ['no', 'n']:
            return False
        print("Invalid input. Please enter 'yes' or 'no' (y/n).")

def evaluate_patient():
    print("=== Quick Patient Screening Tool ===\n")
    
    
    while True:
        try:
            systolic_bp = int(input("Enter the patient's Systolic Blood Pressure (top number): "))
            if systolic_bp > 0:
                break
            print("Please enter a valid positive number.")
        except ValueError:
            print("Invalid input. Please enter a whole number (e.g., 120).")
            
  
    has_pain = ask_yes_no("Is the patient experiencing arm pain? (y/n): ")
    
    
    on_dialysis = ask_yes_no("Is the patient currently undergoing dialysis treatment? (y/n): ")

 
    print("\n=== Medical Consultation ===")
    
  
    if systolic_bp >= 180:
        print("🚨 EMERGENCY ALERT: This is a Hypertensive Crisis level blood pressure (Systolic ≥ 180).")
        print("Seek emergency medical attention immediately.")
        return
    elif systolic_bp < 90:
        print("⚠️ ALERT: The patient has low blood pressure (Hypotension).")
        if on_dialysis:
            print("During dialysis, sudden drops in blood pressure can cause severe muscle cramping and dizziness.")
            print("Notify the dialysis nursing staff immediately to adjust fluid removal rates.")
        else:
            print("Ensure the patient is sitting or lying down safely to prevent fainting, and contact a doctor.")
        return


    if has_pain and on_dialysis:
        print("• Status: Arm pain in an active dialysis patient.")
        print("• Advice: Inform the dialysis care team right away. This requires immediate checking")
        print("  of the vascular access site for complications, infiltration, or reduced blood flow.")
    elif has_pain and not on_dialysis:
        print("• Status: Arm pain present, patient not on active dialysis.")
        print("• Advice: Rest the arm and monitor for other symptoms. If the pain is severe,")
        print("  radiates from the chest, or is accompanied by numbness, seek immediate care.")
    elif not has_pain and on_dialysis:
        print("• Status: Patient on dialysis, no arm pain reported.")
        print("• Advice: Blood pressure is stable. Continue monitoring the patient routinely.")
    else:
        print("• Status: Patient is stable. No immediate medical action required based on these fields.")

    print("\n⚠️ REMINDER: Dialysis patients must never take over-the-counter NSAIDs (like ibuprofen)")
    print("without direct approval from their nephrologist.")

evaluate_patient()
