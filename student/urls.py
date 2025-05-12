from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_student, name='add-student'),
    path('results/', views.result_list, name='result-list'),
    path('student/login/', views.student_login, name='student_login'),
]
