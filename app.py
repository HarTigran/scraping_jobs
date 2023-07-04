from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import csv
import sqlite3
import secrets

# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Flask application
app = Flask(__name__)
app.secret_key = secret_key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User class
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Helper function to initialize the SQLite database
def initialize_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    # Create the jobs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            company TEXT,
            location TEXT,
            tag TEXT,
            link TEXT,
            deadline TEXT,
            requirements TEXT,
            outcome TEXT,
            action TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

# Initialize the database
initialize_database()

@login_manager.user_loader
def load_user(user_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Fetch the user from the database
    cursor.execute('SELECT id, username FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    if result:
        user_id, username = result
        return User(user_id, username)

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('job_list'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Fetch the user from the database
        cursor.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        if result and result[2] == password:
            user_id, username, _ = result
            user = User(user_id, username)
            login_user(user)
            return redirect(url_for('job_list'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('job_list'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        user_id = cursor.lastrowid

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

        # Create the User object and login the user
        user = User(user_id, username)
        login_user(user)

        return redirect(url_for('job_list'))

    return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/job_list', methods=['GET', 'POST'])
@login_required
def job_list():
    if request.method == 'POST':
        # Retrieve the form data
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        tag = request.form['tag']
        link = request.form['link']

        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Check if the job already exists in the database
        cursor.execute('SELECT job_id FROM jobs WHERE user_id = ? AND title = ?', (current_user.id, title))
        result = cursor.fetchone()

        if result:
            # Job already exists
            conn.close()
            return 'This job is already in your list.'

        # Insert the new job into the database
        cursor.execute('''
            INSERT INTO jobs (user_id, title, company, location, tag, link)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (current_user.id, title, company, location, tag, link))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

        return redirect(url_for('job_list'))

    # Fetch job listings from the CSV file
    job_listings = []
    with open('job_listings.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            job_listings.append(row)

    return render_template('job_list.html', job_listings=job_listings)

@app.route('/my_job_list', methods=['GET', 'POST'])
@login_required
def my_job_list():
    if request.method == 'POST':
        job_id = request.form['job_id']
        outcome = request.form.get('outcome', '')
        deadline = request.form.get('deadline', '')  # Retrieve the 'deadline' value from the form data
        action = request.form.get('action', '')
        requirements = request.form.get('requirements', '')

        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Update the job outcome and deadline in the database
        cursor.execute('UPDATE jobs SET deadline = ?, requirements = ?, outcome = ?, action = ? WHERE job_id = ?', (deadline, requirements, outcome, action, job_id))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

    # Connect to the SQLite database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Fetch the user's jobs from the database
    cursor.execute('SELECT * FROM jobs WHERE user_id = ?', (current_user.id,))
    user_jobs = cursor.fetchall()

    # Close the connection
    conn.close()

    return render_template('my_job_list.html', user_jobs=user_jobs)

@app.route('/update_job', methods=['POST'])
@login_required
def update_job():
    job_id = request.form['job_id']
    action = request.form['action']

    # Connect to the SQLite database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Update the job action in the database
    cursor.execute('UPDATE jobs SET action = ? WHERE job_id = ?', (action, job_id))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    return redirect(url_for('my_job_list'))

@app.route('/update_deadline', methods=['POST'])
def update_deadline():
    job_id = request.json.get('jobId')
    deadline = request.json.get('deadline')

    # Connect to the SQLite database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Update the deadline in the jobs table for the specified job_id
    cursor.execute('UPDATE jobs SET deadline = ? WHERE job_id = ?', (deadline, job_id))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    return jsonify(success=True)

@app.route('/delete_job', methods=['POST'])
def delete_job():
    job_id = request.form['job_id']
    print(job_id)

    # Connect to the SQLite database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Delete the job row with the specified job_id
    cursor.execute("DELETE FROM jobs WHERE job_id = ?", (job_id,))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect back to the job list page
    return redirect('/job_list')

if __name__ == '__main__':
    app.run(debug=False)
