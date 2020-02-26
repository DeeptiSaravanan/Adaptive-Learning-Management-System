from django import forms
from .models import *

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'USERNAME',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'PASSWORD',
        max_length = 32,
        widget = forms.PasswordInput()
    )
    # preference = forms.ChoiceField(required=True, widget=forms.RadioSelect(
    # attrs={'class': 'Radio'}), choices=(('Books','Books'),('Notes','Notes'),('Videos','Videos'),))
   
class Loginform(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'USERNAME',
        max_length = 32
    )
    password = forms.CharField(
        required = True,
        label = 'PASSWORD',
        max_length = 32,
        widget = forms.PasswordInput()
    )
