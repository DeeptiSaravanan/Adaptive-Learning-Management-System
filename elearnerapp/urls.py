from django.urls import path

from . import views

urlpatterns = [
    path('login', views.pagelogin, name='pagelogin'),
    path('register', views.register, name='register'),
    path('<str:username>/dashboard/<str:subject>/<str:unit>',views.dashboard,name='dashboard'),
    path('post/ajax/timer/',views.write_to_csv,name='write_to_csv'),
    path('<str:username>/<int:questionnaire_id>/diagnostic', views.diagnostic, name='diagnostic'),
]