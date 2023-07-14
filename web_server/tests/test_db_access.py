import unittest
from unittest.mock import MagicMock, call, ANY
from db_access import DBAccess
from datetime import date, datetime

class DBAccessTestCase(unittest.TestCase):
    def setUp(self):
        # Create a mock SQLiteDB instance
        self.mock_db = MagicMock()
        self.db_access = DBAccess()
        # Replace the SQLiteDB instance with the mock
        self.db_access.db = self.mock_db

    def test_insert_to_db(self):
        # Mock data
        user_id = 123
        results = [
            {'text': 'Sample Text 1', 'total_calorie': 100},
            {'text': 'Sample Text 2', 'total_calorie': 200},
            {'text': 'Sample Text 3', 'total_calorie': 300}
        ]

        # Call the method to be tested
        self.db_access.insert_to_db(user_id, results)

        # Assert that the insert method of the mock database was called with the correct arguments
        expected_calls = [
            call.insert(user_id=user_id, transcribed_text='Sample Text 1', translated_text='', calories=100, food_table='', timestamp=ANY, date=str(date.today()), time=ANY),
            call.insert(user_id=user_id, transcribed_text='Sample Text 2', translated_text='', calories=200, food_table='', timestamp=ANY, date=str(date.today()), time=ANY),
            call.insert(user_id=user_id, transcribed_text='Sample Text 3', translated_text='', calories=300, food_table='', timestamp=ANY, date=str(date.today()), time=ANY)
        ]
        
        # Check each call separately
        self.mock_db.assert_has_calls(expected_calls)

    def test_get_items(self):
        # Mock data
        user_id = '123'

        # Mock the return value of get_items() method
        mock_results = [('2023-07-13', 1310)]
        self.mock_db.get_items.return_value = mock_results

        # Call the method to be tested
        result = self.db_access.get_calorie(user_id)

        # Assert the result
        expected_result = [{'date': '2023-07-13', 'calorie': 1310}]
        self.assertEqual(result, expected_result)

        # Assert that the get_items method of the mock database was called with the correct argument
        self.mock_db.get_items.assert_called_once_with(user_id=123)

    def tearDown(self):
        # Clean up resources after each test
        self.db_access = None
        self.mock_db = None

if __name__ == '__main__':
    unittest.main()
