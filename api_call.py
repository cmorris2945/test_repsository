from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy.exc import SQLAlchemyError
from app import app, db, Patient

# Initialize Flask-Restful API
api = Api(app)

class PatientResource(Resource):
    def get(self, patient_id=None):
        if patient_id:
            patient = Patient.query.get_or_404(patient_id)
            return jsonify({
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'sex': patient.sex,  # Add this line
                'stage': patient.stage,
                'previous_treatments': patient.previous_treatments,
                'preferred_language': patient.preferred_language,
                'location': patient.location,
                'family_history': patient.family_history,
                'genetic_testing': patient.genetic_testing,
                'religiosity': patient.religiosity,
                'immigration_status': patient.immigration_status,
                'social_support': patient.social_support,
                'treatment_approach': patient.treatment_approach,  # Add this line
                'doctor_preferences': patient.doctor_preferences,
                'additional_concerns': patient.additional_concerns
            })
        else:
            patients = Patient.query.all()
            result = []
            for patient in patients:
                result.append({
                    'id': patient.id,
                    'name': patient.name,
                    'age': patient.age,
                    'sex': patient.sex,  # Add this line
                    'stage': patient.stage,
                    'previous_treatments': patient.previous_treatments,
                    'preferred_language': patient.preferred_language,
                    'location': patient.location,
                    'family_history': patient.family_history,
                    'genetic_testing': patient.genetic_testing,
                    'religiosity': patient.religiosity,
                    'immigration_status': patient.immigration_status,
                    'social_support': patient.social_support,
                    'treatment_approach': patient.treatment_approach,  # Add this line
                    'doctor_preferences': patient.doctor_preferences,
                    'additional_concerns': patient.additional_concerns
                })
            return jsonify(result), 200

    def post(self):
        try:
            data = request.get_json()
            new_patient = Patient(
                name=data.get('name'),
                age=data.get('age'),
                sex=data.get('sex'),  # Add this line
                stage=data.get('stage'),
                previous_treatments=data.get('previous_treatments'),
                preferred_language=data.get('preferred_language'),
                location=data.get('location'),
                family_history=data.get('family_history'),
                genetic_testing=data.get('genetic_testing'),
                religiosity=data.get('religiosity', ''),
                immigration_status=data.get('immigration_status', ''),
                social_support=data.get('social_support', ''),
                treatment_approach=data.get('treatment_approach', ''),  # Add this line
                doctor_preferences=data.get('doctor_preferences', ''),
                additional_concerns=data.get('additional_concerns', '')
            )
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
api.add_resource(PatientResource, '/api/patients', '/api/patients/<int:patient_id>')

if __name__ == '__main__':
    app.run(debug=True)