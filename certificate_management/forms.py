from django import forms
from .models import Certificate,DuplicateRequest

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['student']

#duplicateCertificate
class DuplicateRequestForm(forms.ModelForm):
    class Meta:
        model = DuplicateRequest
        fields = ['reg_no', 'full_name', 'email', 'reason', 'id_proof']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
