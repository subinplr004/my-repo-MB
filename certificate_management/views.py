from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import CertificateForm,DuplicateRequestForm
from .utils import generate_certificate_pdf
from django.contrib import messages

def issue_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']

            # 🛑 Check for existing valid certificate
            existing = Certificate.objects.filter(student=student, is_revoked=False)
            if existing.exists():
                existing.update(is_revoked=True)
                messages.warning(request, "⚠️ Previous certificate was revoked for this student.")

            # 🔐 Proceed with new certificate
            certificate = form.save(commit=False)
            certificate.cert_id = certificate.generate_cert_id()
            certificate.save()
            generate_certificate_pdf(certificate)

            messages.success(request, "✅ New certificate issued successfully.")
            return render(request, 'certificate_management/certificate_issued.html', {'certificate': certificate})
    else:
        form = CertificateForm()
    return render(request, 'certificate_management/issue_certificate.html', {'form': form})


def verify_certificate(request, cert_id):
    certificate = get_object_or_404(Certificate, cert_id=cert_id)
    is_valid = (certificate.generate_hash() == certificate.hash_value and not certificate.is_revoked)
    calculated_hash = certificate.generate_hash()
    is_valid = calculated_hash == certificate.hash_value and not certificate.is_revoked
    print("Expected:", certificate.hash_value)
    print("Actual:", certificate.generate_hash())
    return render(request, 'certificate_management/verify_result.html', {
        'certificate': certificate,
        'is_valid': is_valid,
    })
    
def verify_certificate_form(request):
    cert = None
    is_valid = None
    if request.method == "POST":
        cert_id = request.POST.get("cert_id")
        try:
            cert = Certificate.objects.get(cert_id=cert_id)
            is_valid = (cert.generate_hash() == cert.hash_value and not cert.is_revoked)
        except Certificate.DoesNotExist:
            cert = None
            is_valid = False
    return render(request, 'certificate_management/verify_form.html', {
        'cert': cert,
        'is_valid': is_valid

    })

#duplicateCertificate
def request_duplicate_certificate(request):
    if request.method == 'POST':
        form = DuplicateRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'certificate_management/request_submitted.html')
    else:
        form = DuplicateRequestForm()
    return render(request, 'certificate_management/duplicate_request.html', {'form': form})

# admin approval for duplicate certificate
from django.contrib.auth.decorators import login_required
@login_required
def duplicate_requests_admin(request):
    requests = DuplicateRequest.objects.order_by('-submitted_at')
    return render(request, 'certificate_management/duplicate_requests_admin.html', {
        'requests': requests
    })

from .models import Certificate, DuplicateRequest
from .utils import generate_certificate_pdf
from django.core.files import File
from io import BytesIO
from django.core.mail import send_mail

@login_required
def update_duplicate_request_status(request, request_id, new_status):
    req = get_object_or_404(DuplicateRequest, id=request_id)

    # ✅ Update status
    req.status = new_status
    req.save()

    # ✅ Auto-issue certificate if approved
    if new_status == 'Approved':
        # Check if a certificate already exists
        existing = Certificate.objects.filter(student__reg_no=req.reg_no, is_revoked=False)
        if existing.exists():
            existing.update(is_revoked=True)

        # Get student record by reg_no
        from student.models import Student
        student = Student.objects.filter(reg_no=req.reg_no).first()

        if student:
            cert = Certificate(student=student)
            cert.cert_id = cert.generate_cert_id()
            cert.hash_value = cert.generate_hash()
            cert.generate_qr_code()
            cert.save()
            generate_certificate_pdf(cert)
            # 🔜 Will add email next

 

    return redirect('admin-duplicate-requests')
