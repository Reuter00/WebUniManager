from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.myarea, name='myarea'),
    path('<str:selected_schoolyear>', views.myarea, name='schoolyear'),
    path('admin/', views.adminpage, name='admin')

]
