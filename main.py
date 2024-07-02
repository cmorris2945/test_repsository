from Flask import Flask, render_template, request, redirect, url_for



app = Flask(__name__)

## Sample data store for POC

patients = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('patient_form', methods['GET', 'POST'])
def patient_form():
    if request.method == 'POST':
        patient_data = {
            'name':request.form['name'],
            'age':request.form['age'],
            'gender':request.form['gender'],
            'disease_stage':request.form['disease_stage'],
            'preference':request.form['preference'],
            'location':request.form['location'],
            'insurance':request.form['insurance']

        }
        ## Save the data back to a database...
        return "Form submitted successfully"
    return render_template("patient_form.html")


if __name__ == "__main__":
    app.run(debug=True)