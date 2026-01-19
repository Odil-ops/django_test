from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Subject,
    Module,
    Question,
    Choice,
    TestAttempt,
    UserResponse,
)


# ---------- Inline ----------
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    verbose_name = _("Choice")
    verbose_name_plural = _("Choices")


# ---------- Question ----------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("short_text", "module")
    list_filter = ("module__subject", "module")
    search_fields = ("text",)
    inlines = [ChoiceInline]

    @admin.display(description=_("Question"))
    def short_text(self, obj):
        return obj.text[:60]


# ---------- Subject ----------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
    ordering = ("name",)


# ---------- Module ----------
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "level")
    list_filter = ("subject", "level")
    search_fields = ("title",)
    ordering = ("subject", "level")


# ---------- Test Attempt ----------
@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ("full_name", "module", "score", "started_at")
    list_filter = ("module__subject", "started_at")
    search_fields = ("full_name",)
    ordering = ("-started_at",)


# ---------- User Response ----------
@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "selected_choice", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("question__text",)


# ---------- Admin global settings ----------
admin.site.site_header = _("Test Platform Administration")
admin.site.site_title = _("Test Platform Admin")
admin.site.index_title = _("Administration")
