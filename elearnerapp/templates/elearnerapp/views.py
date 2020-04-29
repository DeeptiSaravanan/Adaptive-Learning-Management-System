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
from lrupdate import diag_pass,diag_fail
from finish_button import calc
from django.http import JsonResponse



# Create your views here.
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def diagnostic(request,username,subject,unit):
    qid_map={'Introduction':1,'Planning':1,'Organising':1,'Directing':1,'Controlling':1,'Perspectives':8,'BestFit':9,'Introduction to Marketing':3, 'Training':10, 'EmpInterest':11,'Marketing Strategy':4, 'Marketing Mix Decisions':5,'Evaluation':12,'Buyer Behaviour':6,'Marketing Research and Trends in Marketing':7}
    questionnaire_id=qid_map[unit]
    questionnaire=get_object_or_404(Questionnaire,pk=questionnaire_id)
    title_map={'Introduction':'Introduction','Planning':'Planning','Organising':'Organising','Directing':'Directing','Controlling':'Controlling','Perspectives':'Perspectives','BestFit':'BestFit','Introduction to Marketing':'Intro_marketing', 'Training':'Training', 'EmpInterest':'EmpInterest','Marketing Strategy':'Strategy', 'Marketing Mix Decisions':'MixDecisions','Evaluation':'Evaluation','Buyer Behaviour':'Behaviour','Marketing Research and Trends in Marketing':'Trends'}
    unit=title_map[unit]
 
    if request.method == "POST":
        form=Answerform(questionnaire.question_set.all(),request.POST)
        if form.is_valid(): ## Will only ensure the option exists, not correctness.

            results=[]
            score=0
            questionSet=questionnaire.question_set.all()
            q_count=questionSet.count()

            for question in questionSet:
                question_num = "question_%d" % question.pk
                correct_ans=question.correct
                user_ans=form.cleaned_data[question_num]
                if correct_ans==user_ans:
                    is_correct=True
                    score=score+1
                else:
                    is_correct=False
                temp=UserAnswer(ques=question,answer=user_ans,is_correct=is_correct)
                results.append(temp)
            score=round((score*100)/q_count,2)

            user_obj=User.objects.get(username=username)
            user_id=user_obj.pk
            if score>70:
                status="Pass"
                # diag_pass(user_id,unit,score)
            else:
                status="Fail"
                # diag_fail(user_id,unit)
            if subject=="BM":
                full_sub ="Basics of Management"
            elif subject=="MM":
                full_sub="Marketing Management"
            else:
                full_sub="Human Resource Management"
            return render(request,'elearnerapp/result.html',{"results": results,"score":score,"username":username,"status":status,"full_sub":full_sub,"subject":subject,"unit":unit})
    else:
        q_count=questionnaire.question_set.all().count()
        form=Answerform(questions=questionnaire.question_set.all())
    return render(request,'elearnerapp/diagnostic.html', {"form": form,"username":username,"q_count":q_count})


@csrf_exempt 
def write_to_csv(request):
    print("inside write to csv")
    time=request.POST.get('timer',None)
    subject=request.POST.get('subject',None)
    level=request.POST.get('level',None)
    mode=request.POST.get('mode',None)
    username=request.POST.get('username',None)
    unit=request.POST.get('unit',None)
    feedback=request.POST.get('score',None) #write to user feedback csv
    user_obj=User.objects.get(username=username)
    userid=user_obj.pk

    bool_diag =calc(userid,time,mode,level,subject)
    print("inside view1",bool_diag)

    if bool_diag:
        return JsonResponse({
                    'success': True,
                    'url': reverse('content', args=[username,subject,unit]),
                })
    return JsonResponse({ 'success': False, 'url2': reverse('diagnostic', args=[username,subject,unit]), })

def dashboard(request,username):
    return render(request,'elearnerapp/dashboard.html',{"username":username})


def content(request,username,subject,unit):
    #eligible 0 if BM diag has not been taken, 1 if BM diag has been taken and failed, 2 if taken and passed
    # if subject=="MM" or subject="HR" and eligible==0:
    #     return redirect(reverse('diagnostic', args=[username,"BM","Introduction"]))
    Dict = {'Easy': ['Introduction','Planning','Perspectives','BestFit','Introduction to Marketing'],'Medium':['Organising', 'Directing', 'Training', 'EmpInterest','Marketing Strategy', 'Marketing Mix Decisions'],'Hard':['Controlling','Evaluation','Buyer Behaviour','Marketing Research and Trends in Marketing']}
    if(any(unit in x for x in Dict['Easy'])):
        level=0.2
    elif(any(unit in x for x in Dict['Medium'])):
        level=0.5
    elif(any(unit in x for x in Dict['Hard'])):
        level=0.9        
    book_data= pandas.read_csv("C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\"+subject+"_books.csv")
    youtube_data = Ysearch(unit) 
    article_data = Asearch(subject,unit)
    if subject=="BM":
        full_sub ="Basics of Management"
    elif subject=="MM":
        full_sub="Marketing Management"
    else:
        full_sub="Human Resource Management"
    return render(request,'elearnerapp/content_dashboard.html', {"full_sub":full_sub,"username": username,"books":book_data,"videos":youtube_data,"articles":article_data,"subject":subject,"level":level,"unit":unit})

            
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
