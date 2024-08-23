from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import func, case, text
import urllib

db = SQLAlchemy()

# Configure Azure SQL Database connection
server = 'drbotserver.database.windows.net'
database = 'drbothealthdb'
username = 'drbot'
password = 'TheFlash40'
driver = '{ODBC Driver 18 for SQL Server}'

# Create the connection string for Azure
azure_params = urllib.parse.quote_plus(
    f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;'
)

class User(db.Model, UserMixin):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

class Patient(db.Model):
    __bind_key__ = 'azure'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    stage = db.Column(db.String(50), nullable=False)
    previous_treatments = db.Column(db.String(200))
    preferred_language = db.Column(db.String(50))
    location = db.Column(db.String(100))
    family_history = db.Column(db.String(50))
    genetic_testing = db.Column(db.String(50))
    help_today = db.Column(db.String(100))
    help_option = db.Column(db.String(100))
    second_opinion = db.Column(db.String(10))
    started_treatment = db.Column(db.String(10))
    zip_code = db.Column(db.String(20))
    insurance_name = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    confirm_info = db.Column(db.String(10))
    religiosity = db.Column(db.String(50))
    immigration_status = db.Column(db.String(50))
    ethnicity = db.Column(db.String(50))
    social_support = db.Column(db.String(50))
    treatment_approach = db.Column(db.String(100))
    doctor_preferences = db.Column(db.String(100))

def get_patient_statistics():
    try:
        total_patients = db.session.query(Patient).count()
        
        age_groups = db.session.query(
            case(
                (Patient.age < 18, '0-17'),
                (Patient.age.between(18, 30), '18-30'),
                (Patient.age.between(31, 50), '31-50'),
                (Patient.age > 50, '51+'),
                else_='Unknown'
            ).label('age_group'),
            func.count('*').label('count')
        ).group_by('age_group').all()

        gender_distribution = db.session.query(Patient.gender, func.count('*')).group_by(Patient.gender).all()
        treatment_history = db.session.query(Patient.previous_treatments, func.count('*')).group_by(Patient.previous_treatments).all()
        genetic_testing = db.session.query(Patient.genetic_testing, func.count('*')).group_by(Patient.genetic_testing).all()
        language_preferences = db.session.query(Patient.preferred_language, func.count('*')).group_by(Patient.preferred_language).all()
        social_support = db.session.query(Patient.social_support, func.count('*')).group_by(Patient.social_support).all()

        return {
            'total_patients': total_patients,
            'age_groups': dict(age_groups),
            'gender_distribution': dict(gender_distribution),
            'treatment_history': dict(treatment_history),
            'genetic_testing': dict(genetic_testing),
            'language_preferences': dict(language_preferences),
            'social_support': dict(social_support)
        }
    except Exception as e:
        print(f"Error in get_patient_statistics: {str(e)}")
        return None

def test_azure_connection():
    try:
        result = db.session.execute(text("SELECT TOP 1 * FROM Patient")).fetchone()
        print(f"Test query result: {result}")
        return True
    except Exception as e:
        print(f"Error testing Azure connection: {str(e)}")
        return False