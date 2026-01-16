from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('subject/<int:pk>/', views.ModuleListView.as_view(), name='modules'),
    path('module/<int:module_id>/start/', views.StartTestView.as_view(), name='start_test'),
    path('module/<int:module_id>/test/', views.TestView.as_view(), name='test'),
    path('attempt/<int:attempt_id>/results/', views.ResultView.as_view(), name='result'),
    path('attempt/<int:attempt_id>/review/', views.ReviewView.as_view(), name='review'),
]
