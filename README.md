# 🧠 Django Mini EMR

## Overview
The **Mini Emr System**  has secure user authentication, role-based access,   handling of patients, doctors, and medical records. It supports  medical charting (e.g., vitals, HPI, assessments), record assignment, and email notification.




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
- **Add, edit, and delete** patient records with searh and filter.
- **Add ,edit and delete** doctor records with seach and filter
- **create and manage** medical record for patient
- **assign medical record** for doctor
- **display** list of assigned medical record for doctor
- **create** and **manage** medical charts  such as vital sign,paient intake ,hpi ,assessment 
- Email capability 

## 🛠 Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default) or any Django-supported database
- **Other Tools**: Bootstrap (for styling)
## 📸🖼️ Snapshot

### 1. Login and Sign Up


<div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/user-attachments/assets/8cfaa0b5-8d57-4424-9187-b6c222c31a7b" alt="login" style="width: 45%;">
    <img src="https://github.com/user-attachments/assets/b3043f9f-d78f-4f08-b6c0-745cecd62394" alt="register" style="width: 50%;">
</div>


### 2. Triage Vs Doctor Role
- on the left side is what is visible for **triage/Receptionist** in the side bar menu, while on the right side is for **doctor**

<div style="display: flex; justify-content: space-between;">
  <img src="https://github.com/user-attachments/assets/1077afa9-d878-4c93-95e7-906672bfe136" alt="login" style="width: 45%;">
    <img src="https://github.com/user-attachments/assets/65d2a992-76b4-495c-b8a5-18700902299e" alt="login" style="width: 45%;">
   
</div>


### 3. Patient List
- Paginated patient list with data table
  <div>
    
    <img src="https://github.com/user-attachments/assets/bdb299d8-f281-4786-9788-ec6498a0ee1f" alt="login" style="width: 70%;">
  </div>



### 4. Patient Craet/update

![patient create](https://github.com/user-attachments/assets/8ddb20dc-4065-45df-8849-b1aff1f9e8ff)





### 5. Doctor Craete/update
- **Create** and **manage**  Doctor ,create new user and assign role **'doctor'**
 <div>
       <img src="https://github.com/user-attachments/assets/d8bdfb49-ca13-4b8b-a3b5-8f06ec6deb46" alt="login" style="width: 90%;">
 
  </div>

### 6. Medical Record Page
- A page that we can search for a **patient** and **fetch** all his/her medical records
 <div>
  
   <img src="https://github.com/user-attachments/assets/dc00aa12-ecc1-4fd6-a082-8f1dfd295117" alt="login" style="width: 90%;">
 
  </div>


### 7. Create New Medical Record
- **create** new medical record and **assign** to a specific doctor
 <div>
      
   <img src="https://github.com/user-attachments/assets/64d56d1f-ebc5-48e4-89ef-910f78c233e9" alt="login" style="width: 90%;">

  </div>


### 8. Doctor's Assigned Medical Record/WorkList
- A specfic **doctor** can view his/her assigned medical record(the doc only sees her worklist)
 <div>
  <img src="https://github.com/user-attachments/assets/256e1b17-49be-46b4-939a-1440e1e5f38b" alt="login" style="width: 90%;">
  </div>

### 9. Manage Medical Charts
- The doctor can update the necessary charts in the **medical diagnosis stage** and in the **treatment** stage
- The first visible chart is **VitalSign**
 <div>

   <img src="https://github.com/user-attachments/assets/8b82fff4-7a60-4689-a4fc-4cea8800c446" alt="login" style="width: 90%;">
  </div>

### 10. Upate HPI , Patient Intake ,Assessment and Plan

 <div>

   <img src="https://github.com/user-attachments/assets/b37a8a9b-f2e2-4400-9daa-d833bda331c1" alt="login" style="width: 90%;">
  </div>




### 11. Email Send

![email sending](https://github.com/user-attachments/assets/deb5f3e7-c5bb-4c71-8972-b5fc2e39cc14)










## ⚙️🛠 Installation

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
