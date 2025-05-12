from django.db import models

STATUS_CHOICES = [
    ("Active", "Active"),
    ("Inactive", "Inactive"),
    ("Graduated", "Graduated"),
]
class Student(models.Model):
    reg_no = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    batch = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    status = models.CharField(choices=STATUS_CHOICES, default="Active", max_length=20)
    
    def __str__(self):
        return self.full_name
    

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_title = models.CharField(max_length=100)
    result = models.CharField(max_length=10, choices=[("PASS", "Pass"), ("FAIL", "Fail")])
    score = models.FloatField()
    date = models.DateField(auto_now_add=True)

    

