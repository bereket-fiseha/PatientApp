# 🧠 Django Patient Registration

## Overview
The **Patient Registration System** is a Django-based web application designed to manage patient information efficiently. It allows users to register, update, and view patient details in a secure and user-friendly interface.


[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Coverage Status](https://img.shields.io/codecov/c/github/bereket-fiseha/PatientApp?label=coverage)](https://codecov.io/gh/bereket-fiseha/PatientApp)
[![Issues](https://img.shields.io/github/issues/bereket-fiseha/PatientApp.svg)](https://github.com//bereket-fiseha/PatientApp/issues)
[![Last Commit](https://img.shields.io/github/last-commit/bereket-fiseha/PatientApp.svg)](https://github.com/bereket-fiseha/PatientApp/commits)
[![Contributors](https://img.shields.io/github/contributors/bereket-fiseha/PatientApp.svg)](https://github.com/bereket-fiseha/PatientApp/graphs/contributors)
[![Stars](https://img.shields.io/github/stars/bereket-fiseha/PatientApp.svg?style=social)](https://github.com/bereket-fiseha/PatientApp/stargazers)
## ✨ Features
- User authentication and authorization.
- Add, edit, and delete patient records with searh and filter.
- Email capability for patient

## 🛠 Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default) or any Django-supported database
- **Other Tools**: Bootstrap (for styling)
## Snapshot
**1.Login and Sign Up** 


**2. Patient List**



**3. Patient Craete/update**


**4. Patient delete**




**5. mail Send**






## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/your-username/patient-registration.git
  cd src
  ```

2. Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

4. Apply migrations:
  ```bash
  python manage.py migrate
  ```

5. Run the development server:
  ```bash
  python manage.py runserver
  ```

6. Open your browser and navigate to:
  ```
  http://127.0.0.1:8000/
  ```


## Folder Structure
```
src/
├── core/
├── patient/  # Main Django app
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```







## License
This project is licensed under the [MIT License](LICENSE).
