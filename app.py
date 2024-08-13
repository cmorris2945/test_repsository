# app.py

from flask import Flask, render_template, request, redirect, url_for
from database import db, init_db, Patient  # Import from database.py

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
init_db(app)

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
            social_support=request.form['social_support'],
            doctor_preferences=request.form['doctor_preferences']
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
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=False, host='0.0.0.0')
