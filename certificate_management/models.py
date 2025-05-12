import hashlib
import qrcode
import uuid
from io import BytesIO
from django.db import models
from django.core.files import File
from student.models import Student

class Certificate(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    cert_id = models.CharField(max_length=64, unique=True)
    issue_date = models.DateField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    hash_value = models.CharField(max_length=256)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_revoked = models.BooleanField(default=False)

    def __str__(self):
        return self.cert_id

    def generate_cert_id(self):
        import uuid
        return f"MB-{self.student.reg_no}-{uuid.uuid4().hex[:6]}"

    def generate_hash(self):
        base = f"{self.student.reg_no}{self.student.full_name}{self.issue_date}"
        import hashlib
        return hashlib.sha256(base.encode()).hexdigest()

    def generate_qr_code(self):
        qr_data = f"https://yourdomain.com/certificate/verify-certificate/{self.cert_id}"
        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        filename = f"{self.cert_id}_qr.png"
        self.qr_code.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.cert_id or Certificate.objects.filter(cert_id=self.cert_id).exists():
            self.cert_id = self.generate_cert_id()
        self.hash_value = self.generate_hash()

        if not self.qr_code:
            self.generate_qr_code()

        super().save(*args, **kwargs)


#duplicate certificate
class DuplicateRequest(models.Model):
    reg_no = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    reason = models.TextField()
    id_proof = models.FileField(upload_to='duplicate_requests/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ], default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reg_no} - {self.status}"
