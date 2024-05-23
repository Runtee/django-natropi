from django import forms
from .models import Kyc

class KycForm(forms.ModelForm):
    class Meta:
        model = Kyc
        fields = '__all__'
        exclude=['profile','verified']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        instance = kwargs.get('instance')

        if instance and instance.verified:  # Check if the model is verified
            for field in self.fields.values():
                field.widget.attrs['readonly'] = True