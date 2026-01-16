import random
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from django.utils import timezone
from .models import Subject, Module, Question, Choice, TestAttempt, UserResponse

class HomeView(ListView):
    model = Subject
    template_name = 'quiz/index.html'
    context_object_name = 'subjects'

class ModuleListView(DetailView):
    model = Subject
    template_name = 'quiz/modules.html'
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch modules ordered by level
        context['modules'] = self.object.modules.all().order_by('level')
        return context

class StartTestView(View):
    def get(self, request, module_id):
        module = get_object_or_404(Module, pk=module_id)
        return render(request, 'quiz/start_test.html', {'module': module})

    def post(self, request, module_id):
        module = get_object_or_404(Module, pk=module_id)
        full_name = request.POST.get('full_name')
        if not full_name:
            return render(request, 'quiz/start_test.html', {'module': module, 'error': 'Ismingizni kiriting!'})
        
        request.session['full_name'] = full_name
        return redirect('quiz:test', module_id=module.id)

class TestView(View):
    def get(self, request, module_id):
        module = get_object_or_404(Module, pk=module_id)
        full_name = request.session.get('full_name')
        if not full_name:
            return redirect('quiz:start_test', module_id=module.id)
            
        # Get 20 random questions
        all_questions = list(module.questions.all())
        questions = random.sample(all_questions, min(len(all_questions), 20))
        
        return render(request, 'quiz/test.html', {
            'module': module,
            'questions': questions,
            'full_name': full_name
        })

    def post(self, request, module_id):
        module = get_object_or_404(Module, pk=module_id)
        full_name = request.session.get('full_name', 'Anonymous')
        
        # Create attempt
        attempt = TestAttempt.objects.create(
            full_name=full_name,
            module=module,
            total_questions=0, # Will update below
            started_at=timezone.now()
        )
        
        score = 0
        total = 0
        
        # Process answers
        for key, value in request.POST.items():
            if key.startswith('question_'):
                q_id = int(key.split('_')[1])
                choice_id = int(value)
                
                question = Question.objects.get(pk=q_id)
                selected_choice = Choice.objects.get(pk=choice_id)
                
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += 1
                
                UserResponse.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_choice=selected_choice,
                    is_correct=is_correct
                )
                total += 1
        
        attempt.score = score
        attempt.total_questions = total
        attempt.completed_at = timezone.now()
        attempt.save()
        
        # Clear session to prevent loop
        # del request.session['full_name'] 
        
        return redirect('quiz:result', attempt_id=attempt.id)

class ResultView(DetailView):
    model = TestAttempt
    template_name = 'quiz/results.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'

class ReviewView(DetailView):
    model = TestAttempt
    template_name = 'quiz/review.html'
    context_object_name = 'attempt'
    pk_url_kwarg = 'attempt_id'
