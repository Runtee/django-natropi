from django import forms
from .models import *

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = '__all__'
        exclude=['profile']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})