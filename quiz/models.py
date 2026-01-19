from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Subject name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    icon = models.CharField(
        max_length=50,
        default="fas fa-code",
        help_text=_("FontAwesome icon class"),
        verbose_name=_("Icon")
    )

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.name


class Module(models.Model):

    class Level(models.IntegerChoices):
        BEGINNER = 1, _("Beginner")
        INTERMEDIATE = 2, _("Intermediate")
        ADVANCED = 3, _("Advanced")
        EXPERT = 4, _("Expert")

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name=_("Subject")
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("Module title")
    )
    level = models.IntegerField(
        choices=Level.choices,
        default=Level.BEGINNER,
        verbose_name=_("Level")
    )

    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")

    def __str__(self):
        return f"{self.subject.name} - {self.title} ({self.get_level_display()})"


class Question(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("Module")
    )
    text = models.TextField(
        verbose_name=_("Question text")
    )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.text[:50]


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name=_("Question")
    )
    text = models.CharField(
        max_length=255,
        verbose_name=_("Choice text")
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Is correct")
    )

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    def __str__(self):
        return self.text


class TestAttempt(models.Model):
    full_name = models.CharField(
        max_length=100,
        verbose_name=_("Full name")
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name=_("Module")
    )
    score = models.IntegerField(
        default=0,
        verbose_name=_("Score")
    )
    total_questions = models.IntegerField(
        default=20,
        verbose_name=_("Total questions")
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Started at")
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Completed at")
    )

    class Meta:
        verbose_name = _("Test attempt")
        verbose_name_plural = _("Test attempts")

    def __str__(self):
        return f"{self.full_name} - {self.module} - {self.score}/{self.total_questions}"


class UserResponse(models.Model):
    attempt = models.ForeignKey(
        TestAttempt,
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name=_("Test attempt")
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_("Question")
    )
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Selected choice")
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Is correct")
    )

    class Meta:
        verbose_name = _("User response")
        verbose_name_plural = _("User responses")
