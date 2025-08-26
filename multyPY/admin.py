from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Question, Answer, StudentKey, TeacherKey, 
    Exam, ExamAnswer, FinalExam, FinalExamTable, FinalExamAnswer
)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('base_number', 'multiplier', 'correct_answer', 'created_at')
    list_filter = ('base_number', 'multiplier', 'created_at')
    search_fields = ('base_number', 'multiplier')
    ordering = ('base_number', 'multiplier')
    readonly_fields = ('created_at', 'updated_at')
    
    def correct_answer(self, obj):
        return obj.correct_answer()
    correct_answer.short_description = 'Correct Answer'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_display', 'answer', 'correct', 'date')
    list_filter = ('correct', 'date', 'question__base_number')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('date',)
    
    def question_display(self, obj):
        return f"{obj.question.base_number} × {obj.question.multiplier}"
    question_display.short_description = 'Question'

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('user', 'base_number', 'number_of_correct', 'passed', 'get_percentage', 'date')
    list_filter = ('base_number', 'passed', 'date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('date', 'passed')
    
    def get_percentage(self, obj):
        return f"{obj.get_percentage():.0f}%"
    get_percentage.short_description = 'Score %'

@admin.register(ExamAnswer)
class ExamAnswerAdmin(admin.ModelAdmin):
    list_display = ('exam', 'multiplier', 'answer', 'correct')
    list_filter = ('correct', 'exam__base_number')
    search_fields = ('exam__user__username',)

@admin.register(FinalExam)
class FinalExamAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_correct', 'passed', 'get_percentage', 'date')
    list_filter = ('passed', 'date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('date', 'passed')
    
    def get_percentage(self, obj):
        return f"{obj.get_percentage():.0f}%"
    get_percentage.short_description = 'Score %'

@admin.register(FinalExamTable)
class FinalExamTableAdmin(admin.ModelAdmin):
    list_display = ('examTable', 'base_number', 'number_of_correct')
    list_filter = ('base_number',)
    search_fields = ('examTable__user__username',)

@admin.register(FinalExamAnswer)
class FinalExamAnswerAdmin(admin.ModelAdmin):
    list_display = ('finalExamTablexamTable', 'multiplier', 'answer', 'correct')
    list_filter = ('correct', 'finalExamTablexamTable__base_number')

@admin.register(StudentKey)
class StudentKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_at', 'used_by', 'used_at')
    list_filter = ('created_at', 'used_at')
    search_fields = ('key', 'used_by__username')
    readonly_fields = ('created_at', 'used_at', 'used_by')

@admin.register(TeacherKey)
class TeacherKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_at', 'used_by', 'used_at')
    list_filter = ('created_at', 'used_at')
    search_fields = ('key', 'used_by__username')
    readonly_fields = ('created_at', 'used_at', 'used_by')

# Customize User Admin to show groups
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_groups',)
    
    def get_groups(self, obj):
        return ', '.join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'

# Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site
admin.site.site_header = "MultiPY Administration"
admin.site.site_title = "MultiPY Admin"
admin.site.index_title = "Welcome to MultiPY Administration"
