import unittest

import pandas as pd

from etl import transform


class TransformTests(unittest.TestCase):
    def test_transform_deduplicates_and_adds_labels(self):
        source = pd.DataFrame([
            {
                "job_title": "Data Analyst",
                "salary_in_usd": 80000,
                "experience_level": "EN",
                "work_year": 2023,
                "employment_type": "FT",
                "company_size": "M",
            },
            {
                "job_title": "Data Analyst",
                "salary_in_usd": 80000,
                "experience_level": "EN",
                "work_year": 2023,
                "employment_type": "FT",
                "company_size": "M",
            },
        ])

        result = transform(source)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.loc[0, "experience_level_label"], "Entry-level")
        self.assertEqual(result.loc[0, "employment_type_label"], "Full-time")
        self.assertEqual(result.loc[0, "company_size_label"], "Medium (50-250)")
        self.assertTrue(bool(result.loc[0, "role_category"]))

    def test_transform_filters_missing_and_implausible_salary_rows(self):
        source = pd.DataFrame([
            {
                "job_title": "Data Scientist",
                "salary_in_usd": 120000,
                "experience_level": "SE",
                "work_year": 2023,
                "employment_type": "FT",
                "company_size": "L",
            },
            {
                "job_title": "Data Engineer",
                "salary_in_usd": 1000,
                "experience_level": "MI",
                "work_year": 2023,
                "employment_type": "FT",
                "company_size": "M",
            },
            {
                "job_title": None,
                "salary_in_usd": 90000,
                "experience_level": "MI",
                "work_year": 2023,
                "employment_type": "FT",
                "company_size": "S",
            },
        ])

        result = transform(source)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.loc[0, "job_title"], "Data Scientist")

    def test_transform_marks_non_data_role_false(self):
        source = pd.DataFrame([
            {
                "job_title": "Product Manager",
                "salary_in_usd": 110000,
                "experience_level": "MI",
                "work_year": 2023,
                "employment_type": "FT",
                "company_size": "M",
            }
        ])

        result = transform(source)

        self.assertFalse(bool(result.loc[0, "role_category"]))


if __name__ == "__main__":
    unittest.main()
