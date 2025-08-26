#!/usr/bin/env python
"""
Demo Data Creation Script for MultiPY Examiner Review
Creates demo users and sample data for university project examination
"""
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('/workspaces/multiPY')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multyPY.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from multyPY.models import *

def create_demo_data():
    print("Creating demo data for examiner review...")
    
    # Create Groups
    teacher_group, created = Group.objects.get_or_create(name='teacher')
    student_group, created = Group.objects.get_or_create(name='student')
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@demo.com',
            'is_staff': True,
            'is_superuser': True,
            'first_name': 'Demo',
            'last_name': 'Admin'
        }
    )
    if created:
        admin_user.set_password('examiner_demo_2025')
        admin_user.save()
        print("✓ Created admin user")
    else:
        admin_user.set_password('examiner_demo_2025')
        admin_user.save()
        print("✓ Updated admin user password")
    
    # Create teacher user
    teacher_user, created = User.objects.get_or_create(
        username='teacher_demo',
        defaults={
            'email': 'teacher@demo.com',
            'first_name': 'Demo',
            'last_name': 'Teacher',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        teacher_user.set_password('examiner_demo_2025')
        teacher_user.save()
        teacher_group.user_set.add(teacher_user)
        
        # Add teacher permissions
        exam_content_type = ContentType.objects.get_for_model(Exam)
        final_exam_content_type = ContentType.objects.get_for_model(FinalExam)
        
        # Get all exam permissions
        exam_permissions = Permission.objects.filter(content_type=exam_content_type)
        teacher_user.user_permissions.set(exam_permissions)
        
        # Add final exam permission
        final_exam_permission = Permission.objects.get(
            codename='canFinalExam',
            content_type=final_exam_content_type
        )
        teacher_user.user_permissions.add(final_exam_permission)
        print("✓ Created teacher user with permissions")
    else:
        teacher_user.set_password('examiner_demo_2025')
        teacher_user.save()
        print("✓ Updated teacher user password")
    
    # Create student user
    student_user, created = User.objects.get_or_create(
        username='student_demo',
        defaults={
            'email': 'student@demo.com',
            'first_name': 'Demo',
            'last_name': 'Student',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        student_user.set_password('examiner_demo_2025')
        student_user.save()
        student_group.user_set.add(student_user)
        
        # Add basic exam permission
        permission = Permission.objects.get(
            codename='canExamBase_number1',
            content_type=ContentType.objects.get_for_model(Exam)
        )
        student_user.user_permissions.add(permission)
        print("✓ Created student user with basic permissions")
    else:
        student_user.set_password('examiner_demo_2025')
        student_user.save()
        print("✓ Updated student user password")
    
    # Create demo keys for new registrations
    teacher_key, created = TeacherKey.objects.get_or_create(
        key='TEACHER_DEMO_2025'
    )
    if created:
        print("✓ Created teacher registration key")
    
    student_key, created = StudentKey.objects.get_or_create(
        key='STUDENT_DEMO_2025'
    )
    if created:
        print("✓ Created student registration key")
    
    # Create some sample questions for demonstration
    sample_questions = [
        (2, 3, "[5, 6, 7, 8]"),
        (3, 4, "[10, 11, 12, 13]"),
        (5, 6, "[28, 29, 30, 31]"),
        (7, 8, "[54, 55, 56, 57]"),
    ]
    
    for base, multiplier, options in sample_questions:
        question, created = Question.objects.get_or_create(
            base_number=base,
            multiplier=multiplier,
            options=options
        )
        if created:
            print(f"✓ Created sample question: {base} × {multiplier}")
    
    print("\n" + "="*60)
    print("DEMO DATA CREATION COMPLETE!")
    print("="*60)
    print("Demo Accounts Created:")
    print(f"  Admin:   admin / examiner_demo_2025")
    print(f"  Teacher: teacher_demo / examiner_demo_2025")
    print(f"  Student: student_demo / examiner_demo_2025")
    print("\nRegistration Keys:")
    print(f"  Teacher Key: TEACHER_DEMO_2025")
    print(f"  Student Key: STUDENT_DEMO_2025")
    print("\nAccess URLs:")
    print("  Main App: http://localhost:8000/")
    print("  Admin:    http://localhost:8000/admin/")
    print("="*60)

if __name__ == '__main__':
    create_demo_data()
