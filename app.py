# app.py

from flask import Flask, render_template, request, redirect, url_for
from database import db, init_db, Patient  # Import from database.py
import traceback
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
init_db(app)
migrate = Migrate(app, db)  # Add this line to initialize Flask-Migrate

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Print out all form data
            print("Received form data:")
            for key, value in request.form.items():
                print(f"{key}: {value}")

            # Process form submission
            new_patient = Patient(
                name=request.form.get('name'),
                age=request.form.get('age'),
                stage=request.form.get('stage'),
                previous_treatments=request.form.get('previous_treatments'),
                preferred_language=request.form.get('preferred_language'),
                location=request.form.get('location'),
                family_history=request.form.get('family_history'),
                genetic_testing=request.form.get('genetic_testing'),
                help_today=request.form.get('help_today'),
                help_option=request.form.get('help_option'),
                second_opinion=request.form.get('second_opinion'),
                started_treatment=request.form.get('started_treatment'),
                zip_code=request.form.get('zip_code'),
                insurance_name=request.form.get('insurance_name'),
                gender=request.form.get('gender'),
                confirm_info=request.form.get('confirm_info'),
                religiosity=request.form.get('religiosity'),
                immigration_status=request.form.get('immigration_status'),
                ethnicity=request.form.get('ethnicity'),
                social_support=request.form.get('social_support'),
                treatment_approach=request.form.get('treatment_approach'),
                doctor_preferences=request.form.get('doctor_preferences')
            )
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for('thank_you'))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(traceback.format_exc())
            return "An error occurred while processing your request.", 400
    return render_template('index.html')

# Route for the thank you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True, host='0.0.0.0')  # Set debug=True for more detailed error messages