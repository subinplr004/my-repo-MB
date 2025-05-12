from django.shortcuts import render, redirect
from .models import *
from .forms import StudentForm  # You'll need to create this

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-home')  # or another success page
    else:
        form = StudentForm()
    return render(request, 'student/add_student.html', {'form': form})

def result_list(request):
    results = Result.objects.select_related('student').all()
    return render(request, 'student/result_list.html', {'results': results})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import StudentLoginForm

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('student_dashboard')  # Redirect to student dashboard
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = StudentLoginForm()
    return render(request, 'student_login.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def duplicate_certificate_request(request):
    if not hasattr(request.user, 'student'):
        return redirect('student_login')  # Redirect non-student users

    if request.method == 'POST':
        # Handle form submission, save the request
        pass  # Add logic to handle the request form

    return render(request, 'duplicate_certificate_request.html')
