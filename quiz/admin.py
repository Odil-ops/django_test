from django.contrib import admin
from .models import Subject, Module, Question, Choice, TestAttempt, UserResponse

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_filter = ('module__subject', 'module')
    search_fields = ('text',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'level')
    list_filter = ('subject', 'level')

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'module', 'score', 'started_at')
    list_filter = ('module__subject', 'started_at')

admin.site.register(UserResponse)
