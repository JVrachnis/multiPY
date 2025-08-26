# Quick Start Guide for Examiners

## One-Command Setup
```bash
cd /workspaces/multiPY && ./setup_for_examiner.sh && python manage.py runserver 0.0.0.0:8000
```

## Demo Accounts
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | examiner_demo_2025 |
| Teacher | teacher_demo | examiner_demo_2025 |
| Student | student_demo | examiner_demo_2025 |

## Key URLs
- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Features to Test

### Student Features
1. Login as `student_demo`
2. Practice multiplication tables
3. Take timed exams
4. View personal progress

### Teacher Features  
1. Login as `teacher_demo`
2. View student progress reports
3. Manage exam permissions
4. Monitor class performance

### Admin Features
1. Login as `admin` 
2. Access admin panel
3. Manage users and groups
4. Create registration keys

## Registration Keys (for new accounts)
- Teacher: `TEACHER_DEMO_2025`
- Student: `STUDENT_DEMO_2025`

## Project Highlights
- Django MVT architecture
- Role-based authentication
- Interactive learning system
- Real-time progress tracking
- Bootstrap responsive design
