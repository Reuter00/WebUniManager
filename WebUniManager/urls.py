from django.contrib import admin
from django.urls import path, include
from unimanager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('myarea/', views.myarea, name='myarea'),
    path('login/', views.logout_view, name='logout')
]
