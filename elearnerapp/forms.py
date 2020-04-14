from django import forms
from .models import *
from django.forms import ModelForm
from django.forms import modelform_factory

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

class Answerform(forms.Form):
    def __init__(self,questions,*args, **kwargs):
        self.questions = questions
        super(Answerform, self).__init__(*args, **kwargs) 
        q_no=1
        for question in questions:
            field_name = "question_%d" % question.pk
            choices = []
            choices.append(('A',"A) "+question.option_a))
            choices.append(('B',"B) "+question.option_b))
            choices.append(('C',"C) "+question.option_c))
            choices.append(('D',"D) "+question.option_d))	
            print(choices)
            self.fields[field_name]=forms.ChoiceField(label=str(q_no) +". " +question.q_text, required=False, 
            choices=choices, widget=forms.RadioSelect)
            q_no=q_no+1
	        


