# database.py

from flask_sqlalchemy import SQLAlchemy
import urllib

# Configure Azure SQL Database connection
server = 'drbotserver.database.windows.net'
database = 'drbothealthdb'
username = 'drbot'
password = 'TheFlash40'  # Actual password from the connection string
driver = '{ODBC Driver 18 for SQL Server}'  # Ensure this matches the installed driver

# Create the connection string
params = urllib.parse.quote_plus(
    f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;'
)

# Configure SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

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