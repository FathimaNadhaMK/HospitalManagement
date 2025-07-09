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
![Login Page](screenshots/loginpage.png)

### 🏠 Admin Dashboard
![Admin Dashboard](screenshots/admin_page.png)

### 👩‍⚕️ Doctor Dashboard
![Doctor Dashboard](screenshots/doctor_page.png)

### 🧑 Patient Panel
![Patient Panel](screenshots/patient_page.png)

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
