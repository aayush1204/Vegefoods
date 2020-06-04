from django import forms
from shop.models import Voucher,Society

class loginform(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100,widget=forms.PasswordInput())

class VoucherCreation(forms.ModelForm):
    class Meta:
        model=Voucher
        fields=['voucher_code','voucher_value','society']

class SocietyCreation(forms.ModelForm):
    class Meta:
        model=Society
        fields=['society_name','society_address','society_locality']
