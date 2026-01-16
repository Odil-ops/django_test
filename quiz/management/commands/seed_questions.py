import random
from django.core.management.base import BaseCommand
from quiz.models import Subject, Module, Question, Choice

class Command(BaseCommand):
    help = 'Seeds database with initial data (Subjects, Modules, Questions)'

    def handle(self, *args, **kwargs):
        subjects_data = [
            {'name': 'Python', 'icon': 'fab fa-python', 'desc': 'Python dasturlash tili'},
            {'name': 'HTML', 'icon': 'fab fa-html5', 'desc': 'Hypertext Markup Language'},
            {'name': 'CSS', 'icon': 'fab fa-css3-alt', 'desc': 'Cascading Style Sheets'},
            {'name': 'JavaScript', 'icon': 'fab fa-js', 'desc': 'Web uchun skript tili'},
            {'name': 'Django', 'icon': 'fas fa-server', 'desc': 'Python web framework'},
        ]

        # Ensure subjects exist
        for sub_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=sub_data['name'],
                defaults={'description': sub_data['desc'], 'icon': sub_data['icon']}
            )
            if created:
                self.stdout.write(f"Created Subject: {subject.name}")

            # Create 4 levels for each subject
            for level_code, level_label in Module.LEVEL_CHOICES:
                module_title = f"{subject.name} - {level_label} bosqich"
                module, m_created = Module.objects.get_or_create(
                    subject=subject,
                    level=level_code,
                    defaults={'title': module_title}
                )
                
                # Check if we need to add questions (aiming for 50 per module to total 200 per subject)
                current_count = Question.objects.filter(module=module).count()
                target_count = 50
                
                if current_count < target_count:
                    needed = target_count - current_count
                    self.stdout.write(f"Generating {needed} questions for {module}...")
                    
                    questions_to_create = []
                    choices_to_create = []
                    
                    for i in range(needed):
                        q_text = f"{subject.name} ({level_label}) bo'yicha test savoli #{current_count + i + 1}. To'g'ri javobni belgilang?"
                        question = Question(module=module, text=q_text)
                        question.save() # Save to get ID for choices
                        
                        # Create 4 choices
                        correct_idx = random.randint(0, 3)
                        for c in range(4):
                            is_correct = (c == correct_idx)
                            choice_text = f"Javob varianti {chr(65+c)} ({'To\'g\'ri' if is_correct else 'Xato'})"
                            choice = Choice(question=question, text=choice_text, is_correct=is_correct)
                            choice.save()
                    
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
