import sys
sys.path.append('C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\elearner\\elearnerapp')
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
from django.forms import formset_factory
from youTubeSearch import Ysearch
from articleSearch import Asearch
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def diagnostic(request,username,questionnaire_id):
    questionnaire=get_object_or_404(Questionnaire,pk=questionnaire_id)
    if request.method == "POST":
        form = Answerform(questionnaire.question_set.all(),request.POST)
        print("post")
        if form.is_valid(): ## Will only ensure the option exists, not correctness.
            print("form valid")
            results=[]
            score=0
            questionSet=questionnaire.question_set.all()
            for question in questionSet:
                if question.pk > 3:
                    break
                question_num = "question_%d" % question.pk
                correct_ans=question.correct
                user_ans=form.cleaned_data[question_num]
                if correct_ans==user_ans:
                    is_correct=True
                    score=score+1
                else:
                    is_correct=False
                temp=UserAnswer(ques=question,answer=user_ans,is_correct=is_correct)
                # temp.save()
                results.append(temp)
                # print(results)
            return render(request,'elearnerapp/result.html',{"results": results,"score":score,"username":username})
    else:
        print("get")
        form=Answerform(questions=questionnaire.question_set.all())
    return render(request,'elearnerapp/diagnostic.html', {"form": form,"username":username})


@csrf_exempt 
def write_to_csv(request):
    time=request.POST.get('timer',None)
    subject=request.POST.get('subject',None)
    level=request.POST.get('level',None)
    mode=request.POST.get('mode',None)
    csv_row=[time,level,mode,0.0,0.0,0.0]
    fields=['Time','Level','Mode','NewRate','Rate','Output']
    with open('C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\'+subject+'_NN.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(csv_row)
    f.close()
    return HttpResponse("yay")

def dashboard(request,username):
    return render(request,'elearnerapp/dashboard.html',{"username":username})

def content(request,username,subject,unit):
    Dict = {'Easy': ['Introduction','Planning','Perspectives','BestFit','Introduction to Marketing'],'Medium':['Organising', 'Directing', 'Training', 'EmpInterest','Marketing Strategy', 'Marketing Mix Decisions'],'Hard':['Controlling','Evaluation','Buyer Behaviour','Marketing Research and Trends in Marketing']}
    if(any(unit in x for x in Dict['Easy'])):
        level=0.2
    elif(any(unit in x for x in Dict['Medium'])):
        level=0.5
    elif(any(unit in x for x in Dict['Hard'])):
        level=0.9        
    book_data= pandas.read_csv("C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\"+subject+"_books.csv")
    youtube_data = Ysearch(unit) 
    article_data = Asearch(unit)
    return render(request,'elearnerapp/content_dashboard.html', {"username": username,"books":book_data,"videos":youtube_data,"articles":article_data,"subject":subject,"level":level,"unit":unit})

            
def pagelogin(request):
  
    uservalue=''
    passwordvalue=''

    form= Loginform(request.POST)
    if form.is_valid():
        uservalue= form.cleaned_data.get("username")
        passwordvalue= form.cleaned_data.get("password")
        # user_obj=User.objects.get(username=uservalue)
        user= authenticate(username=uservalue, password=passwordvalue)
        if user is not None:
            login(request, user)

            context= {'form': form}

            messages.success(request, "You have successfully logged in")

            return HttpResponseRedirect('/elearner/'+uservalue+'/dashboard')

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
