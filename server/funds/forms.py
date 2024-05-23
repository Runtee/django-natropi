from django import forms
from .models import Fund

class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['method', 'address', 'trans_hash', 'amount']

class WithdrawForm(forms.Form):
    wallet = forms.ChoiceField(choices=[('main', 'Main'), ('portfolio', 'Portfolio'), ('strategy', 'Strategy'), ('trade', 'Trade')])
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    method = forms.CharField(max_length=100)

class TransferForm(forms.Form):
    from_wallet = forms.ChoiceField(choices=[('main', 'Main'), ('portfolio', 'Portfolio'), ('strategy', 'Strategy'), ('trade', 'Trade')])
    to_wallet = forms.ChoiceField(choices=[('main', 'Main'), ('portfolio', 'Portfolio'), ('strategy', 'Strategy'), ('trade', 'Trade')])
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
