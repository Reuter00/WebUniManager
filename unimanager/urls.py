from django.urls import path

from . import views

urlpatterns = [
    path('', views.myarea, name='myarea'),
    path('<str:selected_schoolyear>', views.myarea, name='schoolyear')
]
