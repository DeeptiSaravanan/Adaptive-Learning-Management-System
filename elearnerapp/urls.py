from django.urls import path

from . import views

urlpatterns = [
    path('login', views.pagelogin, name='pagelogin'),
    path('register', views.register, name='register'),
    path('<str:username>/dashboard',views.dashboard,name='dashboard'),
    path('<str:username>/dashboard/<str:subject>/<str:unit>',views.content,name='content'),
    path('post/ajax/timer/',views.write_to_csv,name='write_to_csv'),
    path('<str:username>/dashboard/<str:subject>/<str:unit>/diagnostic', views.diagnostic, name='diagnostic'),
]