from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.conf import settings
import qrcode
from io import BytesIO
import os
from django.core.files import File


def generate_certificate_pdf(cert):
    filename = f"certificates/{cert.cert_id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Layout
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, "MANBRIDGE ACADEMY")
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height - 130, "Certificate of Completion")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 180, "This is to certify that")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 210, cert.student.full_name)

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 240, f"Reg No: {cert.student.reg_no}")
    c.drawCentredString(width / 2, height - 270, f"Has successfully completed the course:")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 300, f"{cert.student.course} ({cert.student.batch})")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 330, f"Issue Date: {cert.issue_date}")
    c.drawCentredString(width / 2, height - 350, f"Certificate ID: {cert.cert_id}")

    # Generate QR Code (URL to verify page)
    qr = qrcode.make(f"https://yourdomain.com/verify-certificate/{cert.cert_id}")
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)

    # Draw QR on PDF
    c.drawInlineImage(qr_buffer, width - 200, 50, width=100, height=100)

    # Finalize
    c.showPage()
    c.save()
    qr_buffer.close()

    # Save FileField
    with open(file_path, "rb") as f:
        cert.certificate_file.save(f"{cert.cert_id}.pdf", File(f), save=True)
    return filename
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.conf import settings
from django.core.files import File
import os
import qrcode
from io import BytesIO
from PIL import Image  # 🟢 Required fix

def generate_certificate_pdf(cert):
    filename = f"certificates/{cert.cert_id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Certificate Text
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, "MANBRIDGE ACADEMY")
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height - 130, "Certificate of Completion")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 180, "This is to certify that")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 210, cert.student.full_name)
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 240, f"Reg No: {cert.student.reg_no}")
    c.drawCentredString(width / 2, height - 270, f"Has successfully completed the course:")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 300, f"{cert.student.course} ({cert.student.batch})")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 330, f"Issue Date: {cert.issue_date}")
    c.drawCentredString(width / 2, height - 350, f"Certificate ID: {cert.cert_id}")

    # ✅ FIXED QR Code Generation and Embedding
    qr_data = f"https://yourdomain.com/certificate/verify-certificate/{cert.cert_id}"
    qr = qrcode.make(qr_data)
    
    # Convert QR to PIL Image (not BytesIO)
    qr_img = qr.get_image()
    qr_io = BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_io.seek(0)

    pil_image = Image.open(qr_io)
    c.drawInlineImage(pil_image, width - 200, 50, width=100, height=100)

    # Finalize
    c.showPage()
    c.save()

    # Save the PDF to FileField (optional)
    with open(file_path, "rb") as f:
        cert.certificate_file.save(f"{cert.cert_id}.pdf", File(f), save=True)

    return filename
