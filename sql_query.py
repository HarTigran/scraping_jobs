import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('user_database.db')  # Replace 'your_database.db' with the actual database file path
cursor = conn.cursor()

# Query to select all jobs for a specific user (user_id = 1)
user_id = 1  # Replace with the desired user_id
cursor.execute("SELECT * FROM jobs WHERE user_id = ?", (user_id,))
jobs = cursor.fetchall()

# Print the jobs
for job in jobs:
    print(f"Job ID: {job[0]}, User ID: {job[1]}, Title: {job[2]}, Company: {job[3]}, Location: {job[4]}, Tag: {job[5]}, Type: {job[6]}, Link: {job[7]}")

# Close the database connection
conn.close()