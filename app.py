# app.py

from flask import Flask, render_template, request, redirect, url_for
from database import db, init_db, Patient

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
init_db(app)

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Debugging: Print form data to console
            print("Form data received:", request.form)

            # Retrieve form data safely
            name = request.form.get('name')
            age = request.form.get('age')
            sex = request.form.get('sex')
            stage = request.form.get('stage')
            previous_treatments = request.form.get('previous_treatments')
            preferred_language = request.form.get('preferred_language')
            location = request.form.get('location')
            family_history = request.form.get('family_history')
            genetic_testing = request.form.get('genetic_testing')
            religiosity = request.form.get('religiosity', '')
            immigration_status = request.form.get('immigration_status', '')
            social_support = request.form.get('social_support', '')
            treatment_approach = request.form.get('treatment_approach', '')
            doctor_preferences = request.form.get('doctor_preferences', '')
            additional_concerns = request.form.get('additional_concerns', '')

            # Ensure required fields are not None or empty
            if not name or not age or not sex or not stage:
                raise ValueError("Missing required fields")

            # Create a new patient record
            new_patient = Patient(
                name=name,
                age=age,
                sex=sex,
                stage=stage,
                previous_treatments=previous_treatments,
                preferred_language=preferred_language,
                location=location,
                family_history=family_history,
                genetic_testing=genetic_testing,
                religiosity=religiosity,
                immigration_status=immigration_status,
                social_support=social_support,
                treatment_approach=treatment_approach,
                doctor_preferences=doctor_preferences,
                additional_concerns=additional_concerns
            )

            # Add the new patient record to the database
            db.session.add(new_patient)
            db.session.commit()

            # Redirect to the thank you page after successful submission
            return redirect(url_for('thank_you'))

        except Exception as e:
            # Print error to console for debugging
            print("Error:", e)
            # Return a 400 error with a message
            return "An error occurred during form submission. Please check the console for details.", 400

    # Render the main form page
    return render_template('index.html')

# Route for the thank you page
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True, host='0.0.0.0')
