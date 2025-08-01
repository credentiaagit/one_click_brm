# Import required modules
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import logging
import socket
import configparser
import os

# Custom imports
from utils import mongodb_utils, logger_utils, time_utils

# Initialize Flask application
app = Flask(__name__)

# Loading the application configuration 
# Loading the application configuration
app_config = configparser.ConfigParser()
app_config.read('app.config')

# Reading application configurations
app.secret_key = app_config.get('main_application', 'secret_key')

# Injecting the username
@app.context_processor
def inject_username():
    return dict(username=session.get('username'))

# Reading mongodb configurations
mongdb_conn_str = app_config.get('mongodb_database', 'connection_string')
mongdb_dbname = app_config.get('mongodb_database', 'database_name')

# Reading logging configurations
log_level = app_config.get('logging', 'log_level')
log_dir = app_config.get('logging', 'log_dir')
log_filename = app_config.get('logging', 'log_filename')

# Setup loggers
app_logger, func_logger = logger_utils.setup_loggers(
    log_dir=log_dir,
    app_log_filename=log_filename,
    log_level=getattr(logging, log_level.upper(), logging.INFO)
)

@app.before_request
def require_login():
     allowed_routes = ['login', 'signup', 'static']
     if request.endpoint not in allowed_routes and 'username' not in session:
         return redirect(url_for('login'))
#
# Signup Page
# Handles user registration with username and password
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Process form submission for new user registration
    if request.method == 'POST':
        # Get username and password from form data
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists in the database
        existing_user = mongo_db_instance.users.find_one({'username': username})
        if existing_user:
            app_logger.info(f"User {username} already exits.")
            return "User already exists. <a href='/signup'>Try again</a>"

        # Create new user with default 'user' role
        mongo_db_instance.users.insert_one({
            'username': username,
            'password': password,  # In production, passwords should be hashed
            'role': 'user'  # Default role
        })
        app_logger.info(f"User {username} got created successfully.")

        return redirect(url_for('login'))

    # Render the signup form for GET requests
    return render_template('signup.html', hide_sidebar=True)

# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Admin panel
@app.route('/admin', methods=['GET', 'POST'])
def adminpanel():
    users = mongo_db_instance.users.find()
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        mongo_db_instance.users.update_one({"username": username}, {"$set": {"password": new_password}})
        users = mongo_db_instance.users.find()
        app_logger.info(f"{username} : Password updated successfully!");
        return render_template('adminpanel.html', users=users, message="Password updated successfully!")
    return render_template('adminpanel.html', users=users)

# Date to epoch converter
@app.route('/date-to-epoch', methods=['GET', 'POST'])
def date_to_epoch():
    converter = time_utils.DateToEpochConverter()
    result = None
    if request.method == 'POST':
        date_input = request.form['date_input']
        result = converter.convert_to_epoch(date_input)
    current_time = converter.get_current_time()
    return render_template('date_to_epoch.html', result=result, current_time=current_time)

# Login Handler
# Handles user authentication and session management
# Accessible via both /login and / routes
@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    # Process login form submission
    if request.method == 'POST':
        # Get form data with default None if not provided
        username = request.form.get('username')
        password = request.form.get('password')

        # Get database connection and verify user credentials
        user = mongo_db_instance.users.find_one({"username": username, "password": password})

        if user:
            app_logger.info(f"{username} logged in successfully.")
            session['username'] = username  
            # Redirect to dashboard on successful login
            return redirect(url_for('dashboard'))
        else:
            # Log failed login attempt
            app_logger.error(f"Login failed for user: {username}")

    # Render login page for GET requests or failed logins
    return render_template('login.html', hide_sidebar=True)

@app.route('/logout')
def logout():
    username = session.get("username")
    app_logger.info(f"{username} logged out successfully")
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Get the mongodb connection reference
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        try:
            mongo_db_instance = mongodb_utils.get_db(mongdb_conn_str, mongdb_dbname)
            mongo_status = "Connected"
            app_logger.info("MongoDB connected successfully")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            mongo_db_instance = None
            mongo_status = f"Connection failed: {str(e)}"
            app_logger.error(f"MongoDB connection error: {str(e)}")

    app.run(host='0.0.0.0', port=5000, debug=True)
