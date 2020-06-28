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
        fields=['society_name','society_address','society_locality','corporate_discount']

class mailback(forms.Form):
    message=forms.CharField(max_length=250)

class disapprovalform(forms.Form):
    reason=forms.CharField(max_length=100,label='Reason for disapproval')
