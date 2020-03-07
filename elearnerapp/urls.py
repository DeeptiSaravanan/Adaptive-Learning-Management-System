from django.urls import path

from . import views

urlpatterns = [
    path('login', views.pagelogin, name='pagelogin'),
    path('register', views.register, name='register'),
    path('<str:username>/dashboard',views.dashboard,name='dashboard'),
    path('<int:questionnaire_id>/diagnostic', views.diagnostic, name='diagnostic'),
]