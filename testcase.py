import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from tkdatabase import (
    create_database_and_table,
    insert_record,
    check_bill_no_exists,
    read_records_by_field,
    read_records_alike,
    find_records_by_multiple_fields,
    update_record,
    update_release,
    delete_record,
    find_max_bill_no
)

class TestLoanManagement(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_create_database_and_table(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        create_database_and_table()

        mock_connect.assert_called_once()
        mock_connection.cursor().execute.assert_any_call("CREATE DATABASE IF NOT EXISTS loan_management")
        mock_connection.cursor().execute.assert_any_call("USE loan_management")

    @patch('mysql.connector.connect')
    def test_insert_record(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        data = {
            "loan_date": "15-12-2024",
            "bill_no": "B123",
            "name": "John Doe",
            "co_name": "Company A",
            "street": "Main St",
            "address": "City, Country",
            "int_amt": 100.0,
            "weight": 1.2,
            "item": "Gold",
            "no_item": 1,
            "phone_no": "1234567890",
            "release_date": "20-12-2024"
        }

        insert_record(data)

        mock_connect.assert_called_once()
        mock_connection.cursor().execute.assert_called_once()
        self.assertIn("INSERT INTO loan_records", mock_connection.cursor().execute.call_args[0][0])

    @patch('mysql.connector.connect')
    def test_check_bill_no_exists(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor().fetchone.return_value = (1,)

        result = check_bill_no_exists("B123")

        self.assertTrue(result)
        mock_connection.cursor().execute.assert_called_once_with("SELECT COUNT(*) FROM loan_records WHERE bill_no = %s", ("B123",))

    @patch('mysql.connector.connect')
    def test_read_records_by_field(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor(dictionary=True).fetchall.return_value = [
            {"bill_no": "B123", "name": "John Doe"}
        ]

        result = read_records_by_field("name", "John Doe")

        self.assertEqual(result, [{"bill_no": "B123", "name": "John Doe"}])
        mock_connection.cursor().execute.assert_called_once_with("SELECT * FROM loan_records WHERE name = %s", ("John Doe",))

    @patch('mysql.connector.connect')
    def test_update_record(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        updates = {"name": "Jane Doe", "int_amt": 200.0}
        update_record("B123", updates)

        mock_connect.assert_called_once()
        mock_connection.cursor().execute.assert_called_once()
        self.assertIn("UPDATE loan_records SET", mock_connection.cursor().execute.call_args[0][0])

    @patch('mysql.connector.connect')
    def test_delete_record(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        delete_record("B123")

        mock_connect.assert_called_once()
        mock_connection.cursor().execute.assert_called_once_with("DELETE FROM loan_records WHERE bill_no = %s", ("B123",))

    @patch('mysql.connector.connect')
    def test_find_max_bill_no(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor().fetchone.return_value = ("B999",)

        result = find_max_bill_no()

        self.assertEqual(result, "B999")
        mock_connection.cursor().execute.assert_called_once_with("SELECT MAX(bill_no) FROM loan_records")

if __name__ == "__main__":
    unittest.main()
