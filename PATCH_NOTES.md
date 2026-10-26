# Applying this replacement patch

1. Download and extract `project-left-hand-fixed.zip`.
2. Copy the contents of its `project-left-hand-fixed` folder into the root of your existing `project-left-hand` repository, allowing replacement of files with the same names.
3. Delete the old `main (1).py`; the corrected command-line file is now `main.py`.
4. In the project folder, run `python -m py_compile logic.py app.py main.py test_logic.py` and `python -m unittest -v`.
5. Install dependencies with `pip install -r requirements.txt`, then run the web app with `streamlit run app.py`.
6. Review the changed files, then commit and push them to GitHub when you are satisfied.

The test suite validates code behaviour, not medical accuracy. The revised app is still an educational prototype and needs review by a qualified clinician before any broader use.
