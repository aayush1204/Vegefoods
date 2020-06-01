from django import forms

from .models import Signup

class LoginForm(forms.ModelForm):

    class Meta:
        model = Signup
        fields = ('email','password')