from django.shortcuts import render
from unimanager.models import *
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


def myarea(request):
    students = StudentSubject.objects.filter(student=2)  # replace with student that made the login

    context = {
        'students': students
    }

    return render(request, 'unimanager/myarea.html', context)
