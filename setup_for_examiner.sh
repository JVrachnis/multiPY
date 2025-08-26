#!/bin/bash
echo "================================================================"
echo "MultiPY - Multiplication Learning System Setup"
echo "Setting up project for examiner review..."
echo "================================================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "🗄️  Setting up database..."
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Failed to run migrations"
    exit 1
fi

echo "👥 Creating demo users and data..."
python create_demo_data.py

if [ $? -ne 0 ]; then
    echo "❌ Failed to create demo data"
    exit 1
fi

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "================================================================"
echo "✅ SETUP COMPLETE!"
echo "================================================================"
echo ""
echo "🚀 To start the server, run:"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "🌐 Then visit:"
echo "   Main Application: http://localhost:8000"
echo "   Admin Panel:      http://localhost:8000/admin"
echo ""
echo "🔑 Demo Accounts:"
echo "   Admin:   admin / examiner_demo_2025"
echo "   Teacher: teacher_demo / examiner_demo_2025"
echo "   Student: student_demo / examiner_demo_2025"
echo ""
echo "📋 Registration Keys (for creating new accounts):"
echo "   Teacher Key: TEACHER_DEMO_2025"
echo "   Student Key: STUDENT_DEMO_2025"
echo ""
echo "================================================================"
