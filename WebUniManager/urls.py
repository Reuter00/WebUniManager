from django.contrib import admin
from django.urls import path, include
from unimanager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('myarea/', include('unimanager.urls')),
    path('logout/', views.logout_view, name='logout')
]
