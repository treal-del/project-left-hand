# Project Left Hand

A cardiac risk screening tool for dialysis patients.

> **Not medical advice.** This is an educational project. It does not diagnose
> anything. If someone has chest pain, trouble breathing, or feels very unwell,
> call your local emergency number immediately.

## Why

My grandfather survived six years of dialysis. We monitored his kidneys
obsessively. Then his heart killed him in 24 hours because no one connected the
pain in his left hand to the blockages in his arteries. This tool is the first
step toward fixing that gap.

## What it does

- Screens for cardiac risk from blood pressure, arm pain, chest symptoms and
  dialysis status
- Flags hypertensive crisis (systolic above 180) and hypotension (below 90)
  as emergencies
- Treats chest pain, breathlessness or sweating as an emergency
- Asks which arm hurts: pain at the dialysis access points to an access
  problem, pain in the other arm can be a warning sign of a heart problem
- Reminds dialysis patients not to take NSAIDs without nephrologist approval

## Risk levels

| Level | When |
|---|---|
| Emergency | Chest symptoms, systolic above 180, or systolic below 90 |
| High | BP of 140 or more with arm pain or dialysis, or arm pain away from the access site on dialysis |
| Moderate | BP of 140 or more, or on dialysis, or arm pain |
| Low | None of the above |

These thresholds are simplified screening rules, not clinical guidelines.

## Project layout

| File | Purpose |
|---|---|
| `logic.py` | All risk rules, shared by both versions |
| `app.py` | Streamlit web app |
| `main.py` | Command-line version |
| `test_logic.py` | Tests for the rules |
| `requirements.txt` | Dependencies for deployment |

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py      # web app
python main.py            # command-line version
python test_logic.py      # run the tests
```

## Tech

Python and Streamlit.

## Status

v0.2: shared logic module, chest symptom check, access-arm question, tests.

## Ideas for next

- Add ECG-related questions (heart rhythm, palpitations)
- Review the rules with a doctor or nephrologist before sharing widely
