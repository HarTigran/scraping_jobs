import sqlite3

# Replace "your_database.db" with the actual path to your SQLite database file
database_file = "user_database.db"

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a SQL query to retrieve data from the "mentor" table
    cursor.execute("SELECT * FROM mentors")
    rows = cursor.fetchall()

    # Process and display the data
    for row in rows:
        print(row)

except sqlite3.Error as e:
    print("SQLite error:", e)

finally:
    # Close the cursor and the database connection
    if conn:
        cursor.close()
        conn.close()