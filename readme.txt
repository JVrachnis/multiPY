# MultiPY - Interactive Multiplication Learning System

## Quick Start for Examiners

### Demo Accounts (FOR EXAMINATION PURPOSES ONLY)
- **Admin Access**: `/admin`
  - Username: `admin`
  - Password: `examiner_demo_2025`

- **Teacher Demo**: 
  - Username: `teacher_demo`
  - Password: `examiner_demo_2025`

- **Student Demo**:
  - Username: `student_demo` 
  - Password: `examiner_demo_2025`

### Quick Setup
```bash
cd /workspaces/multiPY
pip install -r requirements.txt
python manage.py migrate
python create_demo_data.py
python manage.py runserver 0.0.0.0:8000
```

### Access the Application
- Main Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

### Key Features to Test
1. **Student Portal**: Multiplication practice and timed exams
2. **Teacher Portal**: Create questions, view student progress  
3. **Admin Panel**: User management, system overview

### Project Structure
- `multyPY/models.py` - Database models and business logic
- `multyPY/views.py` - Application views and controllers
- `templates/` - HTML templates with Bootstrap styling
- `static/` - CSS, JavaScript, and static assets
