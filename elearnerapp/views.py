from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,authentication,permissions
from rest_framework.renderers import TemplateHTMLRenderer
from django_tables2 import RequestConfig
from django.core.serializers import serialize
import pandas
import csv
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import *
from .models import *
import json
from django.template.defaulttags import register
# Create your views here.
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def dashboard(request):
    # df=pandas.read_csv("C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\elearner\\elearnerapp\\Diagnostic.csv")
    # q= df.set_index('Index').T.to_dict('dict')
    q=Question.objects.all()
    return render(request, 'elearnerapp/dashboard.html', {'q':q})
        # ,'s':s_json,'a':a_json,'b':b_json,'c':c_json,'d':d_json})

# def evaluate(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     selected_choice = request.POST['sample-radio']
    
#     selected_choice.votes += 1
#     selected_choice.save()
       
        
       
            
def pagelogin(request):
  
    uservalue=''
    passwordvalue=''

    form= Loginform(request.POST)
    if form.is_valid():
        uservalue= form.cleaned_data.get("username")
        passwordvalue= form.cleaned_data.get("password")

        user= authenticate(username=uservalue, password=passwordvalue)
        if user is not None:
            login(request, user)

            context= {'form': form}

            messages.success(request, "You have successfully logged in")

            return HttpResponseRedirect('/elearner/dashboard')

            # return HttpResponseRedirect('/dashboard/'+uservalue+'/')

        else:
            context= {'form': form,
                      'error': 'The username and password combination is incorrect'}
            
            return render(request, 'elearnerapp/login.html', context)
    else:
        
        context= {'form': form}
        return render(request, 'elearnerapp/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username=username,email=email, password=password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/elearner/login')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'elearnerapp/register.html', {'form' : form})
