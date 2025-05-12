from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['reg_no', 'full_name', 'email', 'phone', 'course', 'batch', 'status']

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
