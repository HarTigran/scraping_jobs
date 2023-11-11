import sqlite3

# Replace "user_database.db" with the actual path to your SQLite database file
database_file = "user_database.db"

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a SQL query to retrieve data from the "mentors" table
    cursor.execute("SELECT * FROM mentors")

    # Get the column names (headers)
    headers = [description[0] for description in cursor.description]
    print("Headers:", headers)

    # Fetch the first row of data
    first_row = cursor.fetchone()

    # Process and display the data
    if first_row:
        print("First Row:", first_row)

except sqlite3.Error as e:
    print("SQLite error:", e)

finally:
    # Close the cursor and the database connection
    if conn:
        cursor.close()
        conn.close()