from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="fas fa-code", help_text="FontAwesome icon class")

    def __str__(self):
        return self.name

class Module(models.Model):
    LEVEL_CHOICES = [
        (1, 'Boshlang\'ich (Beginner)'),
        (2, 'O\'rta (Intermediate)'),
        (3, 'Yuqori (Advanced)'),
        (4, 'Ekspert (Expert)'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    
    def __str__(self):
        return f"{self.subject.name} - {self.title} ({self.get_level_display()})"

class Question(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    
    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class TestAttempt(models.Model):
    full_name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=20)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.module} - {self.score}/{self.total_questions}"

class UserResponse(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
