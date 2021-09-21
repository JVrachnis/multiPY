from django.db import models
from django.core import validators
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from datetime import datetime
import json

class Question(models.Model):
    base_number = models.IntegerField(blank=False)
    multiplier = models.IntegerField(blank=False)
    options = models.TextField(validators=[validators.int_list_validator],blank=False)

    def correct_answer(self):
        return (self.base_number * self.multiplier)

    def get_option_list(self):
        return json.loads(self.options)
    class Meta:
        unique_together = ('base_number', 'multiplier','options',)

class Answer(models.Model):
    answer = models.IntegerField(blank=False)
    date = models.DateTimeField(default=datetime.now, blank=False)

    question = models.ForeignKey(Question, on_delete=models.CASCADE,blank=False)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE,blank=False)
    correct=models.BooleanField(blank=False)
    def is_correct(self):
        return self.question.correct_answer() == self.answer
class StudentKey(models.Model):
    key = models.CharField(max_length=10)

class TeacherKey(models.Model):
    key = models.CharField(max_length=16)

class Exam(models.Model):
    base_number = models.IntegerField(blank=False)
    number_of_correct = models.IntegerField(default=0,blank=False)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE,blank=False)
    date = models.DateTimeField(default=datetime.now, blank=False)
    class Meta:
        permissions=(('canExamBase_number1','Can Take Exam for The table of 1'),
        ('canExamBase_number2','Can Take Exam for The table of 2'),
        ('canExamBase_number3','Can Take Exam for The table of 3'),
        ('canExamBase_number4','Can Take Exam for The table of 4'),
        ('canExamBase_number5','Can Take Exam for The table of 5'),
        ('canExamBase_number6','Can Take Exam for The table of 6'),
        ('canExamBase_number7','Can Take Exam for The table of 7'),
        ('canExamBase_number8','Can Take Exam for The table of 8'),
        ('canExamBase_number9','Can Take Exam for The table of 9'),
        ('canExamBase_number10','Can Take Exam for The table of 10'),)

class ExamAnswer(models.Model):
    multiplier = models.IntegerField(blank=False)
    answer = models.IntegerField(blank=False)
    correct=models.BooleanField(blank=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,blank=False)


class FinalExam(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE,blank=False)
    class Meta:
        permissions=(('canFinalExam','Can Take Final Exam'),)

class FinalExamTable(models.Model):
    base_number = models.IntegerField(blank=False)
    examTable = models.ForeignKey(FinalExam, on_delete=models.CASCADE,blank=False)

class FinalExamAnswer(models.Model):
    multiplier = models.IntegerField(blank=False)
    answer = models.IntegerField(blank=False)
    correct=models.BooleanField(blank=False)
    finalExamTablexamTable = models.ForeignKey(FinalExamTable, on_delete=models.CASCADE,blank=False)
