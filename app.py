# app.py

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
            additional_concerns=request.form['additional_concerns']
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
        db.create_all()
    app.run(debug=True)
