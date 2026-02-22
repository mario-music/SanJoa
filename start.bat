@echo off
echo ====================================
echo SanJoa Earth Care - Quick Start
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file and add your GEMINI_API_KEY
    pause
)

echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo Populating database with sample data...
python manage.py populate_db

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Admin credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Demo user credentials:
echo   Email: demo@example.com
echo   Password: demo123
echo.
echo Starting development server...
echo.
python manage.py runserver
