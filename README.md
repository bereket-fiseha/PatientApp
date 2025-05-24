# 🧠 Django Patient Registration

## Overview
The **Patient Registration System** is a Django-based web application designed to manage patient information efficiently. It allows users to register, update, and view patient details in a secure and user-friendly interface.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)

## ✨ Features
- User authentication and authorization.
- Add, edit, and delete patient records with searh and filter.
- Email capability for patient

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default) or any Django-supported database
- **Other Tools**: Bootstrap (for styling)

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
## Snapshot
** 1.Login and Sign Up ** 


** 2. Patient List **



** 3. Patient Craete/update **


** 4. Patient delete **




** 5. mail Send **









## License
This project is licensed under the [MIT License](LICENSE).
