from django.urls import path

from . import views

urlpatterns = [
    path('login', views.pagelogin, name='pagelogin'),
    path('register', views.register, name='register'),
    path('<str:username>/dashboard/<str:subject>/<str:unit>',views.dashboard,name='dashboard'),
    path('<str:username>/<int:questionnaire_id>/diagnostic', views.diagnostic, name='diagnostic'),
    path(r'^resourceTime$', views.resourceTimeTaken, name = 'resourceTimeTaken')
]