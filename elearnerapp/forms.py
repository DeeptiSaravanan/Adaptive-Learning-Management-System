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
	    for question in questions:
	    	if question.pk > 3:
	    		break
	    	field_name = "question_%d" % question.pk
	    	choices = []
	    	choices.append(('A',question.option_a))
	    	choices.append(('B',question.option_b))
	    	choices.append(('C',question.option_c))
	    	choices.append(('D',question.option_d))	
	    	self.fields[field_name]=forms.ChoiceField(label=question.q_text, required=True, 
	    	choices=choices, widget=forms.RadioSelect)
	        


