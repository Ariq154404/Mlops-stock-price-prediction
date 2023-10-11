import mysql.connector
from mysql.connector import Error

def create_tables():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
          host='mysql-service',   # Service name as host
          user='root',
          password='ariq123'
        )
        
        if connection.is_connected():
            # Create a cursor object
            cursor = connection.cursor()
            
            # Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS stockDB")
            
            # Use the database
            cursor.execute("USE stockDB")
            
            # Create the 'stock' table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock (
                    time DATETIME PRIMARY KEY,
                    stock_value DOUBLE
                )
            """)
            
            # Create the 'sentiment' table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sentiment (
                    time DATETIME PRIMARY KEY,
                    sentiment DOUBLE
                )
            """)
            
            print("Tables created successfully!")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    create_tables()
