# Breast Cancer Patient-Doctor Matching Application

This Flask-based web application provides a questionnaire for breast cancer patients to help match them with appropriate doctors based on their specific needs and preferences.

## Features

- User-friendly web form for patients to input their information
- Collects relevant medical history and treatment preferences
- Stores patient data securely in a SQLite database
- Responsive design for desktop and mobile devices
- Chatbot interface 

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your system
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Installation

Follow these steps to get your development environment set up:

1. Clone the repository (or download and extract the ZIP file):
   ```
   git clone https://github.com/yourusername/breast-cancer-patient-matching.git
   ```

2. Navigate to the project directory:
   ```
   cd breast-cancer-patient-matching
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Ensure that the `instance` folder is created in the project root directory.

2. The application uses SQLite by default. If you want to use a different database, update the `SQLALCHEMY_DATABASE_URI` in `app.py`.

## Running the Application

1. Make sure you're in the project directory and your virtual environment is activated.

2. Run the Flask application:
   ```
   python app.py
   ```

3. Open a web browser and navigate to `http://localhost:5000` to view the application.

## Project Structure

```
breast-cancer-patient-matching/
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── logo-placeholder.png
│
├── templates/
│   ├── index.html
│   └── thank_you.html
│
├── app.py
├── requirements.txt
└── README.md
```

## Customization

- To change the application's appearance, modify `static/css/styles.css`.
- To add or modify form fields, update `templates/index.html` and `app.py`.
- To change form validation, edit `static/js/script.js`.



