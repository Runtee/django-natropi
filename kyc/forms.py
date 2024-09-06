from django import forms
from .models import KYC

class KYCForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = [
            'document_type', 'document_number', 'document_image',
            'date_of_birth', 'address', 'city', 'state', 'country', 'phone'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'document_image': 'Upload Document (Passport, Driver’s License, National ID Card)',
        }
