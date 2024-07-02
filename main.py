from Flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)

## Sample data store for POC

patients = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('patient_form', methods['GET', 'POST'])
def patient_form():
    