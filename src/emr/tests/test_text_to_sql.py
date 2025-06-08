import unittest

from emr.llm.llmai import text_to_sql
class TestTextToSQL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the model once for all test methods
        cls.model = "gemini-2.0-flash@google"

    def test_get_all_patients(self):
        prompt = "get all patient data"
        expected_sql = "SELECT first_name, last_name, phone_number FROM emr_patient;"
        self.assertEqual(text_to_sql(self.model,prompt).strip().lower(), expected_sql.lower())

    def test_count_medical_records(self):
        prompt = "How many entries of records are present in medical records?"
        expected_sql = "SELECT COUNT(*) FROM emr_medicalrecord;"
        self.assertEqual(text_to_sql(self.model,prompt).strip().lower(), expected_sql.lower())

    def test_filter_by_gender(self):
        prompt = "List first names and phone numbers of all female patients"
        expected_sql = "SELECT first_name, phone_number FROM emr_patient WHERE gender = 'female';"
        self.assertEqual(text_to_sql(self.model,prompt).strip().lower(), expected_sql.lower())

    def test_join_medical_records_for_name(self):
        prompt = "Get all medical records for a patient named John"
        expected_sql = (
            "SELECT mr.* FROM emr_medicalrecord mr"
"JOIN emr_patient p ON mr.patient_id = p.id"
"WHERE p.first_name = 'john';"

        )
        self.assertEqual(normalize_sql(text_to_sql(self.model,prompt).strip().lower()),normalize_sql( expected_sql.lower()))

    def test_recent_medical_records(self):
        prompt = "Show 10 most recent medical records"
        expected_sql = "SELECT * FROM emr_medicalrecord ORDER BY created_at DESC LIMIT 10;"
        self.assertEqual(text_to_sql(self.model,prompt).strip().lower(), expected_sql.lower())



import re

def normalize_sql(sql: str) -> str:
    """
    Normalize SQL for test comparison:
    - Lowercases everything
    - Removes extra whitespace
    - Standardizes table aliases (e.g., 'm' or 'mr' → 'alias1', 'p' → 'alias2')
    - Removes semicolons
    """
    # Lowercase and remove leading/trailing spaces
    sql = sql.strip().lower()

    # Remove all line breaks and extra spaces
    sql = re.sub(r'\s+', ' ', sql)

    # Remove trailing semicolon
    sql = sql.rstrip(';')

    # Standardize table alias for emr_medicalrecord (e.g., m, mr → alias1)
    sql = re.sub(r'\bemr_medicalrecord\s+(as\s+)?\b\w+\b', 'emr_medicalrecord alias1', sql)
    sql = re.sub(r'\balias1\b', 'alias1', sql)  # Ensure consistent reference

    # Standardize table alias for emr_patient (e.g., p → alias2)
    sql = re.sub(r'\bemr_patient\s+(as\s+)?\b\w+\b', 'emr_patient alias2', sql)
    sql = re.sub(r'\balias2\b', 'alias2', sql)

    # Replace any use of former aliases (m, mr, p) with alias1/alias2
    sql = re.sub(r'\b(mr|m)\.', 'alias1.', sql)
    sql = re.sub(r'\bp\.', 'alias2.', sql)

    return sql

if __name__ == '__main__':
    unittest.main()
