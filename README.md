# 🏥 Hospital Management System

A full-stack web-based Hospital Management System built using **Django**, designed to streamline operations for hospitals by providing role-based access for Doctors, Patients, Pharmacists, and Administrators.

---

## 🚀 Features

- 🔒 Role-Based Access Control
- 🩺 Doctor dashboard & prescription updates
- 🧑‍🤝‍🧑 Patient appointments and history
- 💊 Pharmacist medication handling
- 📂 Admin-level user and system management

---

## 📸 Screenshots

### 🔐 Login Page
![Login Page](screenshots/patientlogin.png)

### 🏠 Admin Dashboard
![Admin Dashboard](screenshots/admin-page.png)
![Admin Dashboard](screenshots/admin-page2.png)
![Admin Dashboard](screenshots/admin-page3.png)

### 👩‍⚕️ Doctor Dashboard
![Doctor Dashboard](screenshots/doctor-page.png)
![Doctor Dashboard](screenshots/prescription.png)

### 🧑 Patient Panel
![Patient Panel](screenshots/patient-page.png)

### 🧑 Patient Panel
![Pharmacist Panel](screenshots/pharmacist-page.png)
![Pharmacist Panel](screenshots/medicine-search.png)

> Make sure your screenshots are stored in a folder named `screenshots/` in your repository root.

---

## 🧱 Tech Stack

- Django (Python), HTML, CSS, Bootstrap
- SQLite database

---

## 🛠️ Setup Instructions

```bash
git clone https://github.com/FathimaNadhaMK/HospitalManagement.git
cd HospitalManagement
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
