import mysql.connector
from mysql.connector import Error
from datetime import *

def create_database_and_table():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='root'  # Replace with your MySQL password
        )

        if connection.is_connected():
            print("Connected to MySQL server")

            # Create a cursor object
            cursor = connection.cursor()

            # Create the database
            database_name = 'loan_management'
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"Database '{database_name}' created or already exists.")

            # Use the database
            cursor.execute(f"USE {database_name}")

            # Define the table name and columns
            table_name = 'loan_records'
            columns = [
                "loan_date DATE",
                "bill_no VARCHAR(50)",
                "name VARCHAR(100)",
                "co_name VARCHAR(100)",
                "street VARCHAR(100) NULL",
                "address VARCHAR(255)",
                "int_amt FLOAT",
                "weight FLOAT",
                "item VARCHAR(100)",
                "no_item INT",
                "phone_no VARCHAR(15) NULL",
                "release_date DATE NULL"
            ]

            # Create the table
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {', '.join(columns)}
            )
            """
            cursor.execute(create_table_query)
            print(f"Table '{table_name}' created or already exists.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

def insert_record(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            table_name = 'loan_records'
            data["loan_date"]=(datetime.strptime((data["loan_date"]),"%d-%m-%Y")).strftime("%Y-%m-%d")
            # columns = [
            #     "loan_date", "bill_no", "name", "co_name", "street", "address",
            #     "int_amt", "weight", "item", "no_item", "phone_no"
            # ]
            placeholders = ', '.join(['%s'] * len(data))
            insert_query = f"INSERT INTO {table_name} ({', '.join(list(data.keys()))}) VALUES ({placeholders})"

            cursor.execute(insert_query, list(data.values()))
            connection.commit()
            print("Record inserted successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# def read_records():
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root', 
#             password='root',
#             database='loan_management'
#         )

#         if connection.is_connected():
#             cursor = connection.cursor()
#             select_query = "SELECT * FROM loan_records"
#             cursor.execute(select_query)
#             records = cursor.fetchall()
#             for record in records:
#                 print(record)

#     except Error as e:
#         print(f"Error: {e}")

#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#             print("MySQL connection closed.")

# def read_specific_record(record_id):
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root', 
#             password='root',
#             database='loan_management'
#         )

#         if connection.is_connected():
#             cursor = connection.cursor()
#             select_query = "SELECT * FROM loan_records WHERE id = %s"
#             cursor.execute(select_query, (record_id,))
#             record = cursor.fetchone()
#             if record:
#                 print(record)
#             else:
#                 print(f"Record with ID {record_id} not found.")

#     except Error as e:
#         print(f"Error: {e}")

#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#             print("MySQL connection closed.")

def check_bill_no_exists(bill_no):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            select_query = "SELECT COUNT(*) FROM loan_records WHERE bill_no = %s"
            cursor.execute(select_query, (bill_no,))
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"Bill number {bill_no} exists in the records.")
                return True
            else:
                print(f"Bill number {bill_no} does not exist in the records.")
                return False

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

def read_records_by_field(field_name, field_value):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            select_query = f"SELECT * FROM loan_records WHERE {field_name} = %s"
            cursor.execute(select_query, (field_value,))
            records = cursor.fetchall()
            if records:
                
                # for record in records:
                #     print(record)
                return records
            else:
                print(f"No records found with {field_name} = {field_value}.")
                return False
    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

def read_records_alike(field_name, search_value):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            select_query = f"SELECT * FROM loan_records WHERE {field_name} LIKE %s"
            value_pattern=f"%{search_value}%"
            cursor.execute(select_query, (value_pattern,))
            records = cursor.fetchall()
            if records:
                # for record in records:
                #     print(record)
                return records
            else:
                print(f"No records found matching pattern {value_pattern} in field {field_name}.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

def find_records_by_multiple_fields(filters):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            keys = list(filters.keys())
            like_keys = []
            exact_keys = []
            
            # Separate LIKE and exact match keys
            for key in keys:
                if key in ['name', 'co_name', 'street', 'address']:  # Add fields you want to match with LIKE
                    like_keys.append(key)
                else:
                    exact_keys.append(key)
            
            # Build WHERE clause
            exact_conditions = ' AND '.join([f"{key} = %s" for key in exact_keys])
            like_conditions = ' AND '.join([f"{key} LIKE %s" for key in like_keys])
            
            # Combine conditions
            conditions = []
            values = []
            if exact_conditions:
                conditions.append(exact_conditions)
                values.extend([filters[key] for key in exact_keys])
            if like_conditions:
                conditions.append(like_conditions)
                values.extend([f"%{filters[key]}%" for key in like_keys])
            
            where_clause = ' AND '.join(conditions)
            select_query = f"SELECT * FROM loan_records WHERE {where_clause}"
            
            cursor.execute(select_query, tuple(values))
            records = cursor.fetchall()
            
            if records:
                print("Matching records:")
                return records
                # for record in records:
                #     print(record)
            else:
                print("No records found matching the given criteria.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

        

def update_record(record_id, updates):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            update_query = f"UPDATE loan_records SET {', '.join([f'{key} = %s' for key in updates.keys()])} WHERE bill_no = %s"
            cursor.execute(update_query, list(updates.values()) + [record_id])
            connection.commit()
            print("Record updated successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

def update_release(record_id, rel_date):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            update_query = f"UPDATE loan_records SET release_date=%s WHERE bill_no = %s"
            cursor.execute(update_query, (rel_date ,record_id))
            connection.commit()
            print("Record updated successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

def delete_record(record_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            delete_query = "DELETE FROM loan_records WHERE bill_no = %s"
            cursor.execute(delete_query, (record_id,))
            connection.commit()
            print("Record deleted successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

def find_max_bill_no():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='root',
            database='loan_management'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            select_query = "SELECT MAX(bill_no) FROM loan_records"
            cursor.execute(select_query)
            max_value = cursor.fetchone()[0]
            if max_value:
                print(f"Maximum bill_no: {max_value}")
                return max_value
            elif max_value is None:
                return 0  # Set to 0 if no records exist
            else:
                print("No records found.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# if __name__ == "__main__":
#     create_database_and_table()




    # Example usage
    # insert_record(("2024-12-15", "B123", "John Doe", "Company A", "Main St", "City, Country", 100.0, 1.2, "Gold", 1, "1234567890", "2024-12-20"))
    # read_records()
    # read_specific_record(1)
    # read_records_by_field("name", "John Doe")
    # update_record(1, {"name": "Jane Doe", "int_amt": 200.0})
    # delete_record(1)
