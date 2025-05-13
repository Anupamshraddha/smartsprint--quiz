
from django.contrib import admin
from .models import Course, Quiz, MCQ, Submission, UserAnswer




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    list_filter = ('course',)

@admin.register(MCQ)
class MCQAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'correct_option')
    list_filter = ('quiz',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'submitted_at')
    list_filter = ('quiz', 'submitted_at')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'selected_option', 'is_correct')
