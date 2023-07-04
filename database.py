import sqlite3

# Database file
DB_FILE = 'job_list.db'

def create_users_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT,
                 password TEXT,
                 name TEXT)''')

    conn.commit()
    conn.close()

def create_job_list_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS job_list
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 title TEXT,
                 company TEXT,
                 location TEXT,
                 tag TEXT,
                 link TEXT)''')

    conn.commit()
    conn.close()

def add_user(username, password, name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
              (username, password, name))
    user_id = c.lastrowid

    conn.commit()
    conn.close()

    return user_id

def get_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT id, username, name FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    conn.close()

    return user

def add_job_to_list(user_id, job):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("INSERT INTO job_list (user_id, title, company, location, tag, link) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, job['Title'], job['Company'], job['Location'], job['Tag'], job['Link']))

    conn.commit()
    conn.close()

def get_user_job_list(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM job_list WHERE user_id = ?', (user_id,))
    jobs = cursor.fetchall()
    conn.close()
    return jobs