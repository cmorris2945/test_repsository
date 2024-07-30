# Medical Dashboard

## Overview
The Medical Dashboard is a web-based application designed to streamline and enhance the management of medical records and appointments. It provides a user-friendly interface for doctors and patients to interact, manage appointments, and view medical records.

## Features
- **Doctor Dashboard**: Doctors can view their schedule, manage appointments, and access patient records.
- **Patient Dashboard**: Patients can book, view, and cancel appointments. They can also view their medical records.
- **Notifications**: Real-time notifications for appointment updates and reminders.
- **User Management**: Secure user authentication and profile management for both doctors and patients.

## Project Structure
The project follows a standard Django structure. Below is a brief overview of the main components:

```
MedicalDashboard-main/
├── dashboard/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       ├── base.html
│       └── dashboard/
│           ├── cancel_appointment.html
│           ├── doctor_dashboard.html
│           ├── home.html
│           ├── notifications.html
│           ├── patient_dashboard.html
│           ├── search_patients.html
│           └── view_medical_records.html
├── django_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── medical_dashboard/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── <migration_files>.py
│   └── templates/
│       └── users/
│           ├── login.html
│           └── register.html
├── .gitignore
├── .replit
├── manage.py
├── poetry.lock
├── pyproject.toml
└── requirements.txt
```

## Installation

### Prerequisites
- Python 3.x
- Django
- Poetry (for dependency management)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/MedicalDashboard.git
   cd MedicalDashboard
   ```

2. **Install dependencies**:
   If you are using Poetry, run:
   ```bash
   poetry install
   ```
   Alternatively, you can install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**: Open your browser and go to `http://127.0.0.1:8000/`.

## Usage
- **Doctors**: After logging in, doctors can manage their appointments and view patient records from their dashboard.
- **Patients**: Patients can book, view, and cancel appointments, as well as view their medical records.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome all contributions.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
Special thanks to all the contributors and the open-source community for their support.
