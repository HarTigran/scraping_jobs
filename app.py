from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_mail import Mail, Message
import csv
import sqlite3
import secrets
import os
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import email_m

# Generate a secure secret key
secret_key = secrets.token_hex(16)

# Flask application
app = Flask(__name__)
app.secret_key = secret_key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'clmtcampus@gmail.com'
app.config['MAIL_PASSWORD'] = ""
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True  # True if Port = 465
mail = Mail(app)


# Sample data (you can load this data from a file or a database)
buckets_data = {
    "Bucket #1": [
        "Climate Finance", "Policy Analysis", "Social Impact", "Justice", "Youth Development", "Climate Policy Analysis",
        "Advocacy", "Youth", "Communication", "Digital Marketing", "International Trade", "Investment",
        "Economic Development", "Public Policy & Value Chain Development", "International Sustainable Development",
        "Macroeconomics"
    ],
    "Bucket #2": [
        "Strategy", "Management", "Policy", "Entrepreneurship", "Sustainable Strategy", "Corporate Strategy",
        "ESG and Corporate Sustainability", "Climate Finance", "General Sustainability", "Social Entrepreneurship",
        "Climate Leadership", "Social Entrepreneurship"
    ],
    "Bucket #3": ["Climate Resilience", "Risk Management", "Resilience", "Adaptation", "Coastal Management"],
    "Bucket #4": ["Climate Psychology", "Climate Behavioral Science"],
    "Bucket #5": ["Strategy", "Management", "Chemistry", "Environmental Science", "Sustainable Fashion", "Sustainable Tourism", "Transportation"],
    "Bucket #6": ["Energy", "Energy Policy", "Energy Finance", "Renewable Energy", "Climate and Energy"],
    "Bucket #7": ["Waste Management", "Circular Economy", "Biodiversity", "Ecological Conservation"],
    "Bucket #8": ["Education", "Green Jobs", "Teaching"],
    "Bucket #9": ["Consumer Goods", "Supply Chain Analysis"]
}

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
            job_type TEXT,
            link TEXT,
            deadline TEXT,
            notes TEXT,
            final_outcome TEXT,
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


# Create a mentors table in the SQLite database
def create_mentors_table():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Check if the "mentors" table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mentors';")
    table_exists = cursor.fetchone()

    # # If the "mentors" table exists, drop it
    # if table_exists:
    #     cursor.execute("DROP TABLE mentors;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors (
            mentor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mentor_name TEXT,
            mentor_linkedin TEXT,
            mentor_email TEXT,
            organization TEXT,
            position TEXT,
            pathway TEXT,
            tags TEXT,
            availability INTEGER,
            last_assigned TEXT,
            days_since_last_assigned INTEGER,
            count INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialize the mentors table
create_mentors_table()

@app.route('/populate_mentors', methods=['GET'])
def populate_mentors():
    # Read mentor data from the CSV file and insert it into the mentors table
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    with open('mentor.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            mentor_name = row['Name']
            mentor_linkedin = row['Linkedin account']
            mentor_email = row['Email address']
            organization = row['Organization']
            position = row['Position']
            pathway = row['Pathway']
            tags = row['Tags']
            availability = int(row['Availability'])
            last_assigned = row['LastAssigned']
            days_since_last_assigned = int(row['DaysSinceLastAssigned'])

            # Check if the mentor with the same email already exists
            cursor.execute("SELECT mentor_id FROM mentors WHERE mentor_email = ?", (mentor_email,))
            existing_mentor = cursor.fetchone()

            if not existing_mentor:

                # Insert the mentor data into the mentors table
                cursor.execute('''
                    INSERT INTO mentors (mentor_name, mentor_linkedin, mentor_email, organization, position, pathway, tags, availability, last_assigned, days_since_last_assigned)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (mentor_name, mentor_linkedin, mentor_email, organization, position, pathway, tags, availability, last_assigned, days_since_last_assigned))

    conn.commit()
    conn.close()

    return 'Mentors populated successfully'

# Call the function to populate mentors from the CSV file
populate_mentors()

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

@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/mentor')
def mentor():
    buckets = buckets_data.keys()
    tags = buckets_data  # Define 'tags' as a dictionary
    if current_user.is_authenticated:
        return render_template('mentor.html', buckets=buckets, tags=tags)
    else:
        return redirect(url_for('login'))
    
@app.route('/mentor-list')
def mentor_list():
    if current_user.is_authenticated and current_user.username == 'admin':
        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute a query to select all data from the "mentors" table
        cursor.execute("SELECT * FROM mentors")

        # Fetch all rows as a list of dictionaries
        columns = [column[0] for column in cursor.description]
        mentor_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Close the database connection
        conn.close()

        return render_template('mentor_list.html', is_admin=True, mentor_data=mentor_data)
    else:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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
            return redirect(url_for('home'))
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

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/job_list', methods=['GET', 'POST'])
@login_required
def job_list():
    if request.method == 'POST':
        # Retrieve the job details from the form
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        tag = request.form['tag']
        job_type = request.form['job_type']
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
            INSERT INTO jobs (user_id, title, company, location, tag, job_type, link)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_user.id, title, company, location, tag, job_type, link))

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

    # # Convert job listings to JSON format
    # job_listings_json = json.dumps(job_listings)

    return render_template('main_page.html', job_listings=job_listings)

@app.route('/survey')
@login_required
def survey():
    return render_template('survey.html')


@app.route('/my_job_list', methods=['GET', 'POST'])
@login_required
def my_job_list():
    if request.method == 'POST':
        job_id = request.form['job_id']
        final_outcome = request.form.get('final_outcome', '')
        deadline = request.form.get('deadline', '')
        action = request.form.get('action', '')
        notes = request.form.get('notes', 'Add your notes here')

        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Update the job final outcome, deadline, and notes in the database
        cursor.execute('UPDATE jobs SET deadline = ?, notes = ?, final_outcome = ?, action = ? WHERE job_id = ?', (deadline, notes, final_outcome, action, job_id))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

    if 'deleted_job_id' in session:
        # Remove the deleted job_id from the session
        deleted_job_id = session.pop('deleted_job_id', None)
        
        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Fetch the user's jobs from the database excluding the deleted job
        cursor.execute('SELECT * FROM jobs WHERE user_id = ? AND job_id != ?', (current_user.id, deleted_job_id))
        user_jobs = cursor.fetchall()

        # Close the connection
        conn.close()
    else:
        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Fetch the user's jobs from the database
        cursor.execute('SELECT * FROM jobs WHERE user_id = ?', (current_user.id,))
        user_jobs = cursor.fetchall()

        # Close the connection
        conn.close()

    return render_template('my_job_list.html', user_jobs=user_jobs)

@app.route('/process_data', methods=['POST'])
def process_data():
    # Get the selected buckets and tags from the form
    bucket1 = request.form.get('bucket1')
    tag1 = request.form.getlist('tag1')  # Use getlist to get multiple selected tags
    bucket2 = request.form.get('bucket2')
    tag2 = request.form.getlist('tag2')

    bucket_choice = [bucket1, bucket2]
    tag_choice= tag1 + tag2
    # Connect to the SQLite database
    conn = sqlite3.connect("user_database.db")

    # Specify the SQL query to retrieve data from the "mentors" table
    sql_query = "SELECT * FROM mentors"

    # Use pandas to read data from the database into a DataFrame
    mentordf = pd.read_sql_query(sql_query, conn)

    # Close the database connection
    conn.close()
    
    # mentordf = pd.read_csv("mentor.csv")
    # Convert 'last_assigned' column to datetime if it's not already
    mentordf['last_assigned'] = pd.to_datetime(mentordf['last_assigned'], errors='coerce')
    today = datetime.today()
    # Check if there are any NaT (Not a Timestamp) values after conversion
    if mentordf['last_assigned'].isna().any():
        # Handle missing or invalid datetime values as needed
        # For example, you can drop rows with missing values
        mentordf = mentordf.dropna(subset=['last_assigned'])

    # Calculate the difference in days between today and last_assigned
    timespent = today - mentordf['last_assigned']
    mentordf['days_since_last_assigned'] = timespent.dt.days
    #if last assigned was over a month ago, change Availability back
    mentordf['availability'] = np.where(mentordf['days_since_last_assigned'] > 30, 1, 0)
    #subset df based on availability
    availablementors = mentordf[(mentordf['availability'] == 1) & (mentordf['count'] < 4) ]
    # choose mentors that match buckets and tags
    availablementors['pathway'] = availablementors['pathway'].str.split(', ')
    availablementors['tags'] = availablementors['tags'].str.split(', ')
    # count number of matches
    availablementors['MatchCount_bucket'] = availablementors['pathway'].apply(lambda x: sum(bucket.lower().replace("#", '') in x for bucket in bucket_choice))
    availablementors['MatchCount_tags'] = availablementors['tags'].apply(lambda x: sum(tag.lower() in x for tag in tag_choice))
    availablementors["TotalMatches"]= availablementors['MatchCount_bucket'] + availablementors['MatchCount_tags']

    #Find the mentors with the highest number of matches -- bucket
    max_match_count = availablementors['TotalMatches'].max()
    mentors_with_highest_matches = availablementors[availablementors['TotalMatches'] == max_match_count]

    result = list(mentors_with_highest_matches[['mentor_name','position','organization','mentor_email']].values.tolist()[0])
    session['mentor_email'] = result[3]

    return jsonify(result=result)

@app.route("/send_email", methods=['POST'])
def send_email():
    today_date = datetime.today().date()
    if request.method == 'POST':
        data = request.get_json()
        recipient_email = data.get('user_email')
        full_name = data.get('full_name')
        linkedin_profile = data.get('linkedin_profile')
        short_bio = data.get('short_bio')
        mentor_email = session.get('mentor_email', 'No email found in session')

        msg = Message('Introduction Request', sender='clmtcampus@gmail.com', recipients=[recipient_email])
        msg.body = f"Hello {full_name},\n\nYou have received an introduction request from {linkedin_profile}.\n\nShort Bio: {short_bio}"

        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Update the "coun" column by adding 1 and "last_assigned" column with the current date
        cursor.execute('''
            UPDATE mentors
            SET count = count + 1, last_assigned = ?
            WHERE mentor_email = ?
        ''', (today_date.strftime("%m/%d/%Y"), mentor_email))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

        try:
            mail.send(msg)
            return "Your introduction request email has been sent!"
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return "Invalid request method"

# @app.route('/update_job', methods=['POST'])
# @login_required
# def update_job():
#     job_id = request.form['job_id']
#     action = request.form['action']

#     # Connect to the SQLite database
#     conn = sqlite3.connect('user_database.db')
#     cursor = conn.cursor()

#     # Update the job action in the database
#     cursor.execute('UPDATE jobs SET action = ? WHERE job_id = ?', (action, job_id))

#     # Commit the changes
#     conn.commit()

#     # Close the connection
#     conn.close()

#     return redirect(url_for('my_job_list'))

# @app.route('/update_deadline', methods=['POST'])
# def update_deadline():
#     job_id = request.json.get('jobId')
#     deadline = request.json.get('deadline')

#     # Connect to the SQLite database
#     conn = sqlite3.connect('user_database.db')
#     cursor = conn.cursor()

#     # Update the deadline in the jobs table for the specified job_id
#     cursor.execute('UPDATE jobs SET deadline = ? WHERE job_id = ?', (deadline, job_id))

#     # Commit the changes
#     conn.commit()

#     # Close the connection
#     conn.close()

#     return jsonify(success=True)

if __name__ == '__main__':
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
