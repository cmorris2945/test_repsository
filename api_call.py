# api_call.py
from flask import request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import SQLAlchemyError
from config import app, db

# Initialize Flask-Restful API
api = Api(app)

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
    social_support = db.Column(db.String(50))
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
    schedule_transportation = db.Column(db.String(3))
    social_support_options = db.Column(db.String(100))
    physician_experience = db.Column(db.String(10))
    treatment_cases = db.Column(db.String(10))
    patient_satisfaction = db.Column(db.String(10))
    appointment_wait_time = db.Column(db.String(10))
    proximity = db.Column(db.String(10))
    treatment_approach = db.Column(db.String(50))
    qualities = db.Column(db.String(100))

class PatientResource(Resource):
    def get(self, patient_id=None):
        if patient_id:
            patient = Patient.query.get_or_404(patient_id)
            return jsonify({
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'stage': patient.stage,
                'previous_treatments': patient.previous_treatments,
                'preferred_language': patient.preferred_language,
                'location': patient.location,
                'family_history': patient.family_history,
                'genetic_testing': patient.genetic_testing,
                'additional_concerns': patient.additional_concerns,
                'religiosity': patient.religiosity,
                'immigration_status': patient.immigration_status,
                'social_support': patient.social_support,
                'doctor_preferences': patient.doctor_preferences,
                'consent': patient.consent,
                'help_today': patient.help_today,
                'help_option': patient.help_option,
                'second_opinion': patient.second_opinion,
                'started_treatment': patient.started_treatment,
                'zip_code': patient.zip_code,
                'insurance_name': patient.insurance_name,
                'gender': patient.gender,
                'confirm_info': patient.confirm_info,
                'schedule_appointment': patient.schedule_appointment,
                'schedule_transportation': patient.schedule_transportation,
                'social_support_options': patient.social_support_options,
                'physician_experience': patient.physician_experience,
                'treatment_cases': patient.treatment_cases,
                'patient_satisfaction': patient.patient_satisfaction,
                'appointment_wait_time': patient.appointment_wait_time,
                'proximity': patient.proximity,
                'treatment_approach': patient.treatment_approach,
                'qualities': patient.qualities
            })
        else:
            patients = Patient.query.all()
            result = []
            for patient in patients:
                patient_data = {
                    'id': patient.id,
                    'name': patient.name,
                    'age': patient.age,
                    'stage': patient.stage,
                    'previous_treatments': patient.previous_treatments,
                    'preferred_language': patient.preferred_language,
                    'location': patient.location,
                    'family_history': patient.family_history,
                    'genetic_testing': patient.genetic_testing,
                    'additional_concerns': patient.additional_concerns,
                    'religiosity': patient.religiosity,
                    'immigration_status': patient.immigration_status,
                    'social_support': patient.social_support,
                    'doctor_preferences': patient.doctor_preferences,
                    'consent': patient.consent,
                    'help_today': patient.help_today,
                    'help_option': patient.help_option,
                    'second_opinion': patient.second_opinion,
                    'started_treatment': patient.started_treatment,
                    'zip_code': patient.zip_code,
                    'insurance_name': patient.insurance_name,
                    'gender': patient.gender,
                    'confirm_info': patient.confirm_info,
                    'schedule_appointment': patient.schedule_appointment,
                    'schedule_transportation': patient.schedule_transportation,
                    'social_support_options': patient.social_support_options,
                    'physician_experience': patient.physician_experience,
                    'treatment_cases': patient.treatment_cases,
                    'patient_satisfaction': patient.patient_satisfaction,
                    'appointment_wait_time': patient.appointment_wait_time,
                    'proximity': patient.proximity,
                    'treatment_approach': patient.treatment_approach,
                    'qualities': patient.qualities
                }
                result.append(patient_data)
            return jsonify(result), 200

    def post(self):
        try:
            data = request.get_json()
            new_patient = Patient(**data)
            db.session.add(new_patient)
            db.session.commit()
            return jsonify({'message': 'Patient created successfully'}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    def put(self, patient_id):
        try:
            patient = Patient.query.get_or_404(patient_id)
            data = request.get_json()
            for key, value in data.items():
                setattr(patient, key, value)
            db.session.commit()
            return jsonify({'message': 'Patient updated successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    def delete(self, patient_id):
        try:
            patient = Patient.query.get_or_404(patient_id)
            db.session.delete(patient)
            db.session.commit()
            return jsonify({'message': 'Patient deleted successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

# Adding URL routes for API
api.add_resource(PatientResource, '/api/patients/<int:patient_id>', '/api/patients')

if __name__ == '__main__':
    app.run(debug=True)
