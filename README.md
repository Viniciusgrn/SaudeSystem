# SaudeSystem

SaudeSystem is a Django-based web system designed to manage various healthcare functionalities. The system integrates modules that handle scheduling, registrations, risk classification, user management, and other essential operations for healthcare institutions.

## Table of Contents
- System Features
- Prerequisites
- Installation and Configuration
- Virtual Environment
- Database and Migrations
- Git Management
- Project Structure
- Useful Commands
- References and Documentation

## System Features
- Scheduling: Manage and schedule consultations and procedures.
- Registrations: Add and update patient, professional, and facility records.
- Risk Classification: Module for evaluating and categorizing care activities.
- Permuta Management: Internal control for exchange operations between units.
- Reports and Analytics: Generate reports and monitor service performance.
- Support and Configuration: Ease of system management via environment configuration files.

## Prerequisites
- Python 3.8 or higher
- Django framework (as specified in requirements.txt)
- Git
- Additional libraries such as Requests and pytz (among others listed in requirements.txt)

## Installation and Configuration
**Clone the Repository:**
```bash
git clone <repository_URL>
cd SaudeSystem
```
**Install Dependencies:**
```bash
pip install -r requirements.txt
```
**Environment Setup:**
Configure the required environment variables by copying `.env.example` to `.env`.

## Virtual Environment
**Create the Virtual Environment:**
```bash
python -m venv venv
```
**Activate the Virtual Environment:**
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```
**Deactivate:**
```bash
deactivate
```
**Remove:**
```bash
rmdir venv /s
```

## Database and Migrations
**Apply Existing Migrations:**
```bash
python manage.py migrate
```
**Create New Migrations:**
```bash
python manage.py makemigrations
```
**Apply New Migrations:**
```bash
python manage.py migrate
```

## Git Management
**Update Local Repository:**
```bash
git pull origin main
```
**Push Changes:**
```bash
git push origin main
```

## Project Structure
- manage.py – Django management script
- requirements.txt – List of Python dependencies
- .env – Environment configuration file
- Modules/Apps: scheduling, registrations, riskClassification, permuta, reports, authUser, contact, equipments, esus, pregnant, demandUnit, offeredVacancy

## Useful Commands
- List packages:
```bash
pip list
```
- Freeze dependencies:
```bash
pip freeze > requirements.txt
```
- Install libraries:
```bash
pip install requests pytz
```
- Create a Django app:
```bash
django-admin startapp <app_name>
```

## References and Documentation
- Django: https://docs.djangoproject.com/
- Python: https://docs.python.org/3/
