"""Unit tests for Project Left Hand's non-diagnostic safety guidance."""

import unittest

from logic import (
    ACCESS_CATHETER, ACCESS_FISTULA, ACCESS_GRAFT, ACCESS_UNSURE,
    EMERGENCY, INFORMATION_ONLY, PROMPT_CARE, NSAID_REMINDER,
    assess,
)


class AssessmentTests(unittest.TestCase):
    def test_no_selected_warning_never_returns_low_risk(self):
        result = assess(systolic_bp=120, diastolic_bp=80)
        self.assertEqual(result.status, INFORMATION_ONLY)
        self.assertIn("cannot rule out", " ".join(result.messages).lower())
        self.assertNotIn("low risk", result.headline.lower())
        self.assertFalse(result.emergency)

    def test_no_bp_is_allowed(self):
        result = assess()
        self.assertEqual(result.status, INFORMATION_ONLY)

    def test_chest_discomfort_triggers_emergency_action(self):
        result = assess(chest_discomfort=True)
        self.assertEqual(result.status, EMERGENCY)
        self.assertTrue(result.emergency)
        self.assertIn("call", " ".join(result.messages).lower())

    def test_each_red_flag_triggers_emergency_action(self):
        flags = (
            "shortness_of_breath", "unexplained_upper_body_pain",
            "cold_sweat_nausea_or_lightheadedness", "sudden_neurologic_symptoms",
            "fainting_or_severe_weakness", "feeling_severely_unwell",
            "access_bleeding_uncontrolled",
        )
        for flag in flags:
            with self.subTest(flag=flag):
                self.assertEqual(assess(**{flag: True}).status, EMERGENCY)

    def test_symptom_emergency_not_masked_by_dialysis_or_bp(self):
        result = assess(
            systolic_bp=190, diastolic_bp=125, dialysis=True,
            chest_discomfort=True,
        )
        self.assertEqual(result.status, EMERGENCY)
        self.assertIn("call your local emergency number now", " ".join(result.messages).lower())
        self.assertIn(NSAID_REMINDER, result.messages)

    def test_systolic_above_180_prompts_care_not_automatic_emergency(self):
        self.assertEqual(assess(systolic_bp=181).status, PROMPT_CARE)

    def test_diastolic_above_120_prompts_care(self):
        self.assertEqual(assess(diastolic_bp=121).status, PROMPT_CARE)

    def test_systolic_180_alone_does_not_make_emergency(self):
        self.assertNotEqual(assess(systolic_bp=180).status, EMERGENCY)

    def test_diastolic_120_alone_does_not_make_emergency(self):
        self.assertNotEqual(assess(diastolic_bp=120).status, EMERGENCY)

    def test_high_bp_with_emergency_symptom_is_emergency(self):
        self.assertEqual(
            assess(systolic_bp=181, shortness_of_breath=True).status,
            EMERGENCY,
        )

    def test_low_systolic_prompts_human_advice_not_automatic_emergency(self):
        result = assess(systolic_bp=89)
        self.assertEqual(result.status, PROMPT_CARE)
        self.assertFalse(result.emergency)

    def test_low_systolic_with_fainting_is_emergency(self):
        result = assess(systolic_bp=89, fainting_or_severe_weakness=True)
        self.assertEqual(result.status, EMERGENCY)

    def test_dialysis_adds_medicine_caution(self):
        self.assertIn(NSAID_REMINDER, assess(dialysis=True).messages)
        self.assertNotIn(NSAID_REMINDER, assess(dialysis=False).messages)

    def test_access_site_changes_prompt_dialysis_team(self):
        result = assess(dialysis=True, access_site_changes=True)
        self.assertEqual(result.status, PROMPT_CARE)
        self.assertIn("dialysis team", " ".join(result.messages).lower())

    def test_fistula_vibration_change_is_relevant(self):
        self.assertEqual(
            assess(dialysis=True, access_type=ACCESS_FISTULA,
                   access_vibration_changed=True).status,
            PROMPT_CARE,
        )

    def test_graft_vibration_change_is_relevant(self):
        self.assertEqual(
            assess(dialysis=True, access_type=ACCESS_GRAFT,
                   access_vibration_changed=True).status,
            PROMPT_CARE,
        )

    def test_catheter_dressing_problem_is_relevant_to_catheter(self):
        self.assertEqual(
            assess(dialysis=True, access_type=ACCESS_CATHETER,
                   catheter_or_dressing_problem=True).status,
            PROMPT_CARE,
        )

    def test_catheter_dressing_problem_not_assumed_for_known_fistula(self):
        self.assertEqual(
            assess(dialysis=True, access_type=ACCESS_FISTULA,
                   catheter_or_dressing_problem=True).status,
            INFORMATION_ONLY,
        )

    def test_access_flags_ignored_when_not_on_dialysis(self):
        self.assertEqual(
            assess(dialysis=False, access_type=ACCESS_UNSURE,
                   access_site_changes=True).status,
            INFORMATION_ONLY,
        )

    def test_fever_chills_on_dialysis_prompt_care_team(self):
        self.assertEqual(
            assess(dialysis=True, fever_or_chills=True).status,
            PROMPT_CARE,
        )

    def test_uncontrolled_access_bleeding_is_emergency(self):
        result = assess(dialysis=True, access_bleeding_uncontrolled=True)
        self.assertEqual(result.status, EMERGENCY)
        self.assertIn("steady pressure", " ".join(result.messages).lower())

    def test_negative_bp_rejected(self):
        with self.assertRaises(ValueError):
            assess(systolic_bp=-1)

    def test_zero_bp_must_be_passed_as_none(self):
        with self.assertRaises(ValueError):
            assess(systolic_bp=0)

    def test_boolean_bp_rejected(self):
        with self.assertRaises(ValueError):
            assess(systolic_bp=True)

    def test_non_finite_bp_rejected(self):
        with self.assertRaises(ValueError):
            assess(systolic_bp=float("nan"))

    def test_invalid_access_type_rejected(self):
        with self.assertRaises(ValueError):
            assess(dialysis=True, access_type="other")

    def test_non_boolean_symptom_input_rejected(self):
        with self.assertRaises(ValueError):
            assess(chest_discomfort="yes")


if __name__ == "__main__":
    unittest.main(verbosity=2)
