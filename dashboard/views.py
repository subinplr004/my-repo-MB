from django.shortcuts import render
from student.models import Student, Result
from certificate_management.models import Certificate
# from accounting.models import Fee

def home(request):
    context = {
        'student_count': Student.objects.count(),
        'pass_count': Result.objects.filter(result='PASS').count(),
        'fail_count': Result.objects.filter(result='FAIL').count(),
        'cert_count': Certificate.objects.count(),
        # 'fee_collected': Fee.objects.aggregate(Sum('amount'))['amount__sum'],  # if Fee model exists
    }
    return render(request, 'dashboard/home.html', context)


