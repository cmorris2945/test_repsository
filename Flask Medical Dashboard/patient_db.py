from sqlalchemy import create_engine, Column, Integer, String, func, case, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib

Base = declarative_base()

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

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={azure_params}")
Session = sessionmaker(bind=engine)

class Patient(Base):
    __tablename__ = 'Patient'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    stage = Column(String(50), nullable=False)
    previous_treatments = Column(String(200))
    preferred_language = Column(String(50))
    location = Column(String(100))
    family_history = Column(String(50))
    genetic_testing = Column(String(50))
    help_today = Column(String(100))
    help_option = Column(String(100))
    second_opinion = Column(String(10))
    started_treatment = Column(String(10))
    zip_code = Column(String(20))
    insurance_name = Column(String(50))
    gender = Column(String(20))
    confirm_info = Column(String(10))
    religiosity = Column(String(50))
    immigration_status = Column(String(50))
    ethnicity = Column(String(50))
    social_support = Column(String(50))
    treatment_approach = Column(String(100))
    doctor_preferences = Column(String(100))

def get_patient_statistics():
    session = Session()
    try:
        total_patients = session.query(Patient).count()
        
        age_groups_subquery = session.query(
            case(
                (Patient.age < 18, '0-17'),
                (Patient.age.between(18, 30), '18-30'),
                (Patient.age.between(31, 50), '31-50'),
                (Patient.age > 50, '51+'),
                else_='Unknown'
            ).label('age_group'),
            Patient.id
        ).subquery()

        age_groups = session.query(
            age_groups_subquery.c.age_group,
            func.count(age_groups_subquery.c.id).label('count')
        ).group_by(age_groups_subquery.c.age_group).all()

        gender_distribution = session.query(Patient.gender, func.count('*')).group_by(Patient.gender).all()
        treatment_history = session.query(Patient.previous_treatments, func.count('*')).group_by(Patient.previous_treatments).all()
        genetic_testing = session.query(Patient.genetic_testing, func.count('*')).group_by(Patient.genetic_testing).all()
        language_preferences = session.query(Patient.preferred_language, func.count('*')).group_by(Patient.preferred_language).all()
        social_support = session.query(Patient.social_support, func.count('*')).group_by(Patient.social_support).all()

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
    finally:
        session.close()

def test_azure_connection():
    session = Session()
    try:
        result = session.query(Patient).first()
        print(f"Test query result: {result}")
        return True
    except Exception as e:
        print(f"Error testing Azure connection: {str(e)}")
        return False
    finally:
        session.close()