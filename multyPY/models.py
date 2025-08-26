from django.db import models
from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import datetime
import json

class Question(models.Model):
    base_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Multiplication table base (1-12)"
    )
    multiplier = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Multiplier value (1-12)"
    )
    options = models.TextField(
        validators=[validators.int_list_validator],
        help_text="JSON array of answer options"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def correct_answer(self):
        return (self.base_number * self.multiplier)

    def get_option_list(self):
        try:
            return json.loads(self.options)
        except json.JSONDecodeError:
            return []
    
    def clean(self):
        """Validate that correct answer is in options"""
        from django.core.exceptions import ValidationError
        options = self.get_option_list()
        if self.correct_answer() not in options:
            raise ValidationError("Correct answer must be included in options")
    
    def __str__(self):
        return f"{self.base_number} × {self.multiplier} = {self.correct_answer()}"
    
    class Meta:
        unique_together = ('base_number', 'multiplier', 'options')
        indexes = [
            models.Index(fields=['base_number', 'multiplier']),
            models.Index(fields=['created_at']),
        ]

class Answer(models.Model):
    answer = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        help_text="Student's answer to the question"
    )
    date = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Time taken to answer in seconds"
    )
    
    def is_correct(self):
        return self.question.correct_answer() == self.answer
    
    def save(self, *args, **kwargs):
        """Auto-set correct field based on answer"""
        self.correct = self.is_correct()
        super().save(*args, **kwargs)
    
    def __str__(self):
        status = "✓" if self.correct else "✗"
        return f"{self.user.username}: {self.question} = {self.answer} {status}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['question', 'correct']),
        ]
class StudentKey(models.Model):
    key = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(
        auth_models.User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        status = "Used" if self.used_at else "Available"
        return f"Student Key: {self.key} ({status})"

class TeacherKey(models.Model):
    key = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(
        auth_models.User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        status = "Used" if self.used_at else "Available"
        return f"Teacher Key: {self.key} ({status})"

class Exam(models.Model):
    base_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    number_of_correct = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    time_taken = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Total time taken for exam in seconds"
    )
    passed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        """Auto-set passed status"""
        self.passed = self.number_of_correct >= 5
        super().save(*args, **kwargs)
    
    def get_percentage(self):
        """Get exam score as percentage"""
        return (self.number_of_correct / 10) * 100
    
    def __str__(self):
        return f"{self.user.username} - Table {self.base_number}: {self.number_of_correct}/10"
    
    class Meta:
        permissions = (
            ('canExamBase_number1', 'Can Take Exam for The table of 1'),
            ('canExamBase_number2', 'Can Take Exam for The table of 2'),
            ('canExamBase_number3', 'Can Take Exam for The table of 3'),
            ('canExamBase_number4', 'Can Take Exam for The table of 4'),
            ('canExamBase_number5', 'Can Take Exam for The table of 5'),
            ('canExamBase_number6', 'Can Take Exam for The table of 6'),
            ('canExamBase_number7', 'Can Take Exam for The table of 7'),
            ('canExamBase_number8', 'Can Take Exam for The table of 8'),
            ('canExamBase_number9', 'Can Take Exam for The table of 9'),
            ('canExamBase_number10', 'Can Take Exam for The table of 10'),
        )
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['base_number', 'number_of_correct']),
        ]

class ExamAnswer(models.Model):
    multiplier = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    answer = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    correct = models.BooleanField(default=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    time_taken = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Time taken for this specific answer in seconds"
    )
    
    def __str__(self):
        return f"Exam {self.exam.id}: {self.exam.base_number} × {self.multiplier} = {self.answer}"
    
    class Meta:
        unique_together = ('exam', 'multiplier')
        indexes = [
            models.Index(fields=['exam', 'correct']),
        ]


class FinalExam(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    total_correct = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    time_taken = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Total time taken for final exam in seconds"
    )
    passed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        """Auto-set passed status"""
        self.passed = self.total_correct >= 50
        super().save(*args, **kwargs)
    
    def get_percentage(self):
        """Get final exam score as percentage"""
        return self.total_correct
    
    def __str__(self):
        return f"{self.user.username} - Final Exam: {self.total_correct}/100"
    
    class Meta:
        permissions = (('canFinalExam', 'Can Take Final Exam'),)
        indexes = [
            models.Index(fields=['user', 'date']),
        ]

class FinalExamTable(models.Model):
    base_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    examTable = models.ForeignKey(FinalExam, on_delete=models.CASCADE)
    number_of_correct = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    
    def __str__(self):
        return f"Final Exam {self.examTable.id} - Table {self.base_number}"
    
    class Meta:
        unique_together = ('examTable', 'base_number')

class FinalExamAnswer(models.Model):
    multiplier = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    answer = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    correct = models.BooleanField(default=False)
    finalExamTablexamTable = models.ForeignKey(FinalExamTable, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Final Exam Answer: {self.finalExamTablexamTable.base_number} × {self.multiplier} = {self.answer}"
    
    class Meta:
        unique_together = ('finalExamTablexamTable', 'multiplier')
