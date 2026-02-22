#!/bin/bash

echo "===================================="
echo "SanJoa Earth Care - Quick Start"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file and add your GEMINI_API_KEY"
    read -p "Press enter to continue..."
fi

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Populating database with sample data..."
python manage.py populate_db

echo ""
echo "===================================="
echo "Setup Complete!"
echo "===================================="
echo ""
echo "Admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Demo user credentials:"
echo "  Email: demo@example.com"
echo "  Password: demo123"
echo ""
echo "Starting development server..."
echo ""
python manage.py runserver
