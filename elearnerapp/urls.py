from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('login', views.pagelogin, name='pagelogin'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
]