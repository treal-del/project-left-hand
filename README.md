# Project Left Hand

**An educational cardiac-symptom and dialysis-access awareness checklist.**

> **Important safety notice:** This is a student-built educational project. It is **not medical advice, a diagnosis, a validated screening instrument, or a cardiac-risk calculator**. It cannot rule out a heart problem or tell a person they are safe. If a medical emergency may be happening, call your local emergency number now; do not wait for this tool.

## Why this project exists

Project Left Hand was inspired by a family experience with dialysis and a missed connection between an upper-body symptom and serious heart disease. The aim is to make selected warning signs more visible and encourage people to seek appropriate human help—not to replace clinical judgement.

## What this version does

- Displays an emergency warning before the checklist.
- Allows optional systolic **and** diastolic blood-pressure values.
- Highlights selected symptoms that can indicate a possible emergency and advises calling local emergency services.
- Provides general prompts to contact a dialysis team about access-site changes.
- Distinguishes fistula/graft vibration prompts from catheter/dressing prompts.
- Reminds dialysis patients to ask their nephrology/dialysis team before using common over-the-counter pain medicines such as ibuprofen or naproxen.
- Uses non-diagnostic action guidance instead of high/moderate/low cardiac-risk labels.

## What it deliberately does not do

- It does not calculate cardiac risk or diagnose a heart attack, hypertension, hypotension, or access complication.
- It does not label the user “low risk” or imply that no selected warning means the person is safe.
- It does not treat a blood-pressure number alone as proof of a medical emergency.
- It does not recommend medication changes.
- It has not undergone clinical validation and should not be used to decide whether to delay or avoid professional care.

## Project layout

| File | Purpose |
|---|---|
| `logic.py` | Central, non-diagnostic guidance logic used by both interfaces |
| `app.py` | Streamlit web interface |
| `main.py` | Command-line interface |
| `test_logic.py` | Standard-library unit tests |
| `.github/workflows/tests.yml` | Runs unit tests on pushes and pull requests |
| `requirements.txt` | Streamlit dependency for the web interface |

## Run locally

Use Python 3.10 or later.

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

To run the command-line version:

```bash
python main.py
```

To run unit tests (no third-party test package is required):

```bash
python -m unittest -v
```

## Medical review and limitations

The application's symptom prompts and blood-pressure messages are general safety information adapted from the public resources below. They are **not** patient-specific instructions and have not been reviewed or validated for a particular clinical workflow. The project should receive review by an appropriately qualified clinician—ideally someone familiar with cardiology and dialysis—before any wider use. A clinician should review every prompt, escalation message, access-specific distinction, and the intended audience.

## Educational references

- American Heart Association, [Warning Signs of a Heart Attack](https://www.heart.org/en/health-topics/heart-attack/warning-signs-of-a-heart-attack)
- American Heart Association, [Understanding Blood Pressure Readings](https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings)
- National Kidney Foundation, [Hemodialysis Access](https://www.kidney.org/kidney-topics/hemodialysis-access)
- National Kidney Foundation, [Hemodialysis: How It Works, Types, and What to Expect](https://www.kidney.org/kidney-topics/hemodialysis)

These sources are for general education. They do not validate this application.

## Contributing / future work

Before adding features such as ECG interpretation, predictive models, or patient data collection:

1. Get the current prompts reviewed by a qualified clinician.
2. Define an intended use and a clear safety case.
3. Specify the data sources, privacy safeguards, consent process, and permissions before collecting any user or health data.
4. Add tests and document limitations before changing behaviour.
5. Do not claim diagnostic performance or clinical validity without appropriate study and review.

## Status

Student-built educational prototype. Not clinically validated. Feedback and code review are welcome; clinical use is not intended.
