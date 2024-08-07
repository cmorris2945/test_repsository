from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
db = SQLAlchemy(app)

# Define Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    previous_treatments = db.Column(db.String(200))
    preferred_language = db.Column(db.String(50))
    location = db.Column(db.String(100))
    family_history = db.Column(db.String(50))
    genetic_testing = db.Column(db.String(50))
    additional_concerns = db.Column(db.Text)
    religiosity = db.Column(db.String(50))
    immigration_status = db.Column(db.String(50))
    ethnicity = db.Column(db.String(50))  # New field for ethnicity
    social_support_status = db.Column(db.String(50))  # Updated field for social support status
    doctor_preferences = db.Column(db.String(100))
    consent = db.Column(db.String(3))
    help_today = db.Column(db.String(100))
    help_option = db.Column(db.String(100))
    second_opinion = db.Column(db.String(3))
    started_treatment = db.Column(db.String(3))
    zip_code = db.Column(db.String(10))
    insurance_name = db.Column(db.String(100))
    gender = db.Column(db.String(6))
    confirm_info = db.Column(db.String(3))
    schedule_appointment = db.Column(db.String(3))
    schedule_transportation = db.Column(db.String(10))  # Updated field for schedule transportation
    social_support_options = db.Column(db.String(100))
    physician_experience = db.Column(db.String(10))
    treatment_cases = db.Column(db.String(10))
    patient_satisfaction = db.Column(db.String(10))
    appointment_wait_time = db.Column(db.String(10))
    proximity = db.Column(db.String(10))
    treatment_approach = db.Column(db.String(50))
    qualities = db.Column(db.String(100))

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process form submission
        new_patient = Patient(
            name=request.form['name'],
            age=request.form['age'],
            stage=request.form['stage'],
            previous_treatments=request.form['previous_treatments'],
            preferred_language=request.form['preferred_language'],
            location=request.form['location'],
            family_history=request.form['family_history'],
            genetic_testing=request.form['genetic_testing'],
            additional_concerns=request.form['additional_concerns'],
            religiosity=request.form['religiosity'],
            immigration_status=request.form['immigration_status'],
            ethnicity=request.form['ethnicity'],  # New field for ethnicity
            social_support_status=request.form['social_support_status'],  # Updated field for social support status
            doctor_preferences=request.form['doctor_preferences'],
            consent=request.form.get('consent'),
            help_today=request.form.get('help_today'),
            help_option=request.form.get('help_option'),
            second_opinion=request.form.get('second_opinion'),
            started_treatment=request.form.get('started_treatment'),
            zip_code=request.form['zip_code'],
            insurance_name=request.form['insurance_name'],
            gender=request.form.get('gender'),
            confirm_info=request.form.get('confirm_info'),
            schedule_appointment=request.form.get('schedule_appointment'),
            schedule_transportation=request.form.get('schedule_transportation'),  # Updated field for schedule transportation
            social_support_options=request.form.get('social_support_options'),
            physician_experience=request.form.get('physician_experience'),
            treatment_cases=request.form.get('treatment_cases'),
            patient_satisfaction=request.form.get('patient_satisfaction'),
            appointment_wait_time=request.form.get('appointment_wait_time'),
            proximity=request.form.get('proximity'),
            treatment_approach=request.form.get('treatment_approach'),
            qualities=request.form['qualities']
        )
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('index.html')

# Route for the thank you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
