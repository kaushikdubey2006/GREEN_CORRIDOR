# db.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Establishes and returns a MySQL database connection.
    Compatible with app.py, traffic_controller.py, emergency_handler.py
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",             # MySQL username
            password="Computer@12",  # MySQL password
            database="smart_traffic" # Database name
        )

        if conn.is_connected():
            return conn
        else:
            print("❌ MySQL connected but connection not active")
            return None

    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None
