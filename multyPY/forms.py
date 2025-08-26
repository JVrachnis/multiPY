from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer, Exam

class ExamForm(forms.Form):
    """Form for creating and configuring exams"""
    base_number = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 12,
            'placeholder': 'Enter multiplication table (1-12)'
        }),
        label='Multiplication Table'
    )
    
    time_limit = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 30,
            'placeholder': 'Time limit in minutes'
        }),
        label='Time Limit (minutes)',
        initial=10
    )

class MultipleChoiceAnswerForm(forms.Form):
    """Form for multiple choice answers with validation"""
    answer = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'max': 1000
        }),
        label='Your Answer'
    )

class CustomUserCreationForm(UserCreationForm):
    """Enhanced user registration form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('teacher', 'Teacher')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='I am a'
    )
    
    key = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter registration key'
        }),
        label='Registration Key'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'key')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to default fields
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

class QuestionForm(forms.ModelForm):
    """Form for creating and editing questions"""
    class Meta:
        model = Question
        fields = ['base_number', 'multiplier', 'options']
        widgets = {
            'base_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 12
            }),
            'multiplier': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 12
            }),
            'options': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter options as JSON array, e.g., [6, 7, 8, 9]'
            })
        }

    def clean_options(self):
        """Validate that options is a valid JSON array"""
        import json
        options = self.cleaned_data['options']
        try:
            parsed = json.loads(options)
            if not isinstance(parsed, list):
                raise forms.ValidationError("Options must be a JSON array")
            if len(parsed) < 2:
                raise forms.ValidationError("Must provide at least 2 options")
            return options
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format for options")
