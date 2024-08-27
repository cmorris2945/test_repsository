from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from user_db import User, db
from patient_db import get_patient_statistics, test_azure_connection
from app_factory import create_app

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app, login_manager, db = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        user = User.query.filter_by(email=email, user_type=user_type).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('doctor_dashboard' if user.user_type == 'doctor' else 'patient_dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        full_name = request.form.get('full_name')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, user_type=user_type, full_name=full_name)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error registering user: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if not current_user.is_authenticated or current_user.user_type != 'doctor':
        flash('You must be logged in as a doctor to access this page.', 'error')
        return redirect(url_for('login'))
    
    if not test_azure_connection():
        flash('Unable to connect to the patient database. Please try again later.', 'error')
        return redirect(url_for('login'))
    
    try:
        patient_stats = get_patient_statistics()
        if patient_stats is None:
            flash('An error occurred while fetching patient statistics. Please try again later.', 'error')
            return redirect(url_for('login'))
        app.logger.info(f"Patient stats: {patient_stats}")  # Keep this line for debugging
        return render_template('doctor_dashboard.html', current_user=current_user, patient_demographics=patient_stats)
    except Exception as e:
        app.logger.error(f"Error in doctor_dashboard: {str(e)}")
        flash('An error occurred while loading the dashboard. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    if current_user.user_type != 'patient':
        return redirect(url_for('doctor_dashboard'))
    return render_template('patient_dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001) 
 
