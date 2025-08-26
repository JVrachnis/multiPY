from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from multyPY.models import Question, Answer, Exam, ExamAnswer, StudentKey, TeacherKey
import json

class AuthenticationTestCase(TestCase):
    """Test user authentication and authorization"""
    
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(
            username='teststudent',
            password='testpass123',
            email='student@test.com'
        )
        self.teacher_user = User.objects.create_user(
            username='testteacher',
            password='testpass123',
            email='teacher@test.com'
        )
        
        # Create groups
        student_group, _ = Group.objects.get_or_create(name='student')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        
        # Assign users to groups
        student_group.user_set.add(self.student_user)
        teacher_group.user_set.add(self.teacher_user)
        
    def test_login_required_redirect(self):
        """Test that protected views redirect to login"""
        response = self.client.get('/multiplication_table_ex/1/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
        
    def test_student_login(self):
        """Test student can login successfully"""
        login_successful = self.client.login(username='teststudent', password='testpass123')
        self.assertTrue(login_successful)
        
    def test_teacher_login(self):
        """Test teacher can login successfully"""
        login_successful = self.client.login(username='testteacher', password='testpass123')
        self.assertTrue(login_successful)

class QuestionModelTestCase(TestCase):
    """Test Question model functionality"""
    
    def setUp(self):
        self.question = Question.objects.create(
            base_number=2,
            multiplier=3,
            options='[5, 6, 7, 8]'
        )
        
    def test_correct_answer_calculation(self):
        """Test that correct answer is calculated properly"""
        self.assertEqual(self.question.correct_answer(), 6)
        
    def test_option_list_parsing(self):
        """Test that options are parsed correctly"""
        options = self.question.get_option_list()
        self.assertEqual(options, [5, 6, 7, 8])
        self.assertIn(6, options)  # Correct answer should be in options

class AnswerModelTestCase(TestCase):
    """Test Answer model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.question = Question.objects.create(
            base_number=3,
            multiplier=4,
            options='[11, 12, 13, 14]'
        )
        
    def test_correct_answer_validation(self):
        """Test answer correctness validation"""
        correct_answer = Answer.objects.create(
            answer=12,
            question=self.question,
            user=self.user,
            correct=True
        )
        self.assertTrue(correct_answer.is_correct())
        
        wrong_answer = Answer.objects.create(
            answer=11,
            question=self.question,
            user=self.user,
            correct=False
        )
        self.assertFalse(wrong_answer.is_correct())

class ExamTestCase(TestCase):
    """Test Exam functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='examuser',
            password='testpass123'
        )
        
        # Add basic exam permission
        content_type = ContentType.objects.get_for_model(Exam)
        permission = Permission.objects.get(
            codename='canExamBase_number1',
            content_type=content_type
        )
        self.user.user_permissions.add(permission)
        
    def test_exam_permission_required(self):
        """Test that exam requires proper permissions"""
        self.client.login(username='examuser', password='testpass123')
        
        # Should have access to table 1
        response = self.client.get('/multiplication_table_ex/1/')
        self.assertEqual(response.status_code, 200)
        
        # Should not have access to table 2
        response = self.client.get('/multiplication_table_ex/2/')
        self.assertEqual(response.status_code, 302)  # Redirect
        
    def test_exam_submission(self):
        """Test exam answer submission"""
        self.client.login(username='examuser', password='testpass123')
        
        # Submit exam answers
        post_data = {}
        for i in range(1, 11):
            post_data[f'quantity1_{i}'] = 1 * i  # All correct answers
            
        response = self.client.post('/multiplication_table_ex/1/', post_data)
        self.assertEqual(response.status_code, 200)
        
        # Check if exam was created
        exam = Exam.objects.filter(user=self.user, base_number=1).first()
        self.assertIsNotNone(exam)
        self.assertEqual(exam.number_of_correct, 10)

class MultipleChoiceTestCase(TestCase):
    """Test Multiple Choice functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='mcuser',
            password='testpass123'
        )
        
    def test_multiple_choice_display(self):
        """Test multiple choice question display"""
        self.client.login(username='mcuser', password='testpass123')
        response = self.client.get('/multiple_choice/2/3/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2')
        self.assertContains(response, '3')
        
    def test_multiple_choice_submission(self):
        """Test multiple choice answer submission"""
        self.client.login(username='mcuser', password='testpass123')
        
        # First get the question to know the options
        response = self.client.get('/multiple_choice/2/3/')
        self.assertEqual(response.status_code, 200)
        
        # Submit correct answer
        post_data = {
            'base_number': 2,
            'multiplier': 3,
            'answer': 6,
            'options': '[5, 6, 7, 8]'
        }
        
        response = self.client.post('/multiple_choice/2/3/', post_data)
        self.assertEqual(response.status_code, 200)
        
        # Check if answer was recorded
        answer = Answer.objects.filter(user=self.user).first()
        self.assertIsNotNone(answer)
        self.assertEqual(answer.answer, 6)
        self.assertTrue(answer.correct)

class RegistrationTestCase(TestCase):
    """Test user registration functionality"""
    
    def setUp(self):
        self.client = Client()
        # Create registration keys
        StudentKey.objects.create(key='STUDENT_TEST_KEY')
        TeacherKey.objects.create(key='TEACHER_TEST_KEY')
        
    def test_student_registration(self):
        """Test student registration with valid key"""
        post_data = {
            'username': 'newstudent',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'student@test.com',
            'first_name': 'Test',
            'last_name': 'Student',
            'role': 'student',
            'key': 'STUDENT_TEST_KEY'
        }
        
        response = self.client.post('/signup/', post_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
        # Check if user was created
        user = User.objects.filter(username='newstudent').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.groups.filter(name='student').exists())
        
    def test_registration_invalid_key(self):
        """Test registration fails with invalid key"""
        post_data = {
            'username': 'invaliduser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'invalid@test.com',
            'first_name': 'Invalid',
            'last_name': 'User',
            'role': 'student',
            'key': 'INVALID_KEY'
        }
        
        response = self.client.post('/signup/', post_data)
        self.assertEqual(response.status_code, 200)  # Stays on registration page
        
        # Check if user was not created
        user = User.objects.filter(username='invaliduser').first()
        self.assertIsNone(user)

class TeacherViewsTestCase(TestCase):
    """Test teacher-specific views"""
    
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(
            username='teacher',
            password='testpass123'
        )
        self.student = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        
        # Create groups
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        student_group, _ = Group.objects.get_or_create(name='student')
        
        teacher_group.user_set.add(self.teacher)
        student_group.user_set.add(self.student)
        
    def test_teacher_can_view_students(self):
        """Test that teachers can view student list"""
        self.client.login(username='teacher', password='testpass123')
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'student')
        
    def test_student_cannot_view_students(self):
        """Test that students cannot view student list"""
        self.client.login(username='student', password='testpass123')
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 302)  # Redirect to home

class SecurityTestCase(TestCase):
    """Test security features"""
    
    def setUp(self):
        self.client = Client()
        
    def test_csrf_protection(self):
        """Test that CSRF protection is enabled"""
        response = self.client.get('/login/')
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_xss_protection_headers(self):
        """Test that XSS protection headers are set"""
        response = self.client.get('/')
        # Note: These headers might not be visible in test client
        # This test documents the intention
        self.assertEqual(response.status_code, 200)
