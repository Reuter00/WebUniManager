from django.shortcuts import render, redirect
from unimanager.models import *
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
import datetime


# function to get current year for selected_schoolyear default value
def currentyear():
    now = datetime.datetime.now()
    return now.year


def myarea(request, selected_schoolyear=currentyear()):
    userid = None
    # Variable for School year and semester
    schoolyears = SchoolYear.objects.all().order_by('-year')
    selected_schoolyear_info = SchoolYear.objects.get(year=selected_schoolyear)
    semesters = Semester.objects.all()

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')

    userid = request.user.id
    isstudentorprofessor = request.user.is_student

    if isstudentorprofessor:
        studentinfo = Student.objects.get(student_user_id=userid)
        studentsubjects = StudentSubject.objects.filter(student=studentinfo, schoolyear=selected_schoolyear_info.id)
        studentmarks = SPRelation.objects.filter(student_id__in=studentsubjects.all())

        context = {
            'info': studentinfo,
            'subjects': studentsubjects,
            'currentschoolyears': selected_schoolyear_info,
            'schoolyears': schoolyears,
            'semesters': semesters,
            'studentmarks': studentmarks,



        }

    else:
        professorinfo = Professor.objects.get(teacher_user_id=userid)
        professorsubjects = ProfessorSubject.objects.filter(professor=professorinfo,
                                                            schoolyear=selected_schoolyear_info.id)
        context = {
            'info': professorinfo,
            'subjects': professorsubjects,
            'currentschoolyears': selected_schoolyear_info,
            'schoolyears': schoolyears,
            'semesters': semesters,
        }

    return render(request, 'unimanager/myarea.html', context)


# Logout View
def logout_view(request):
    logout(request)


# Logout View
def adminpage(request):
    return HttpResponseRedirect('/admin/')
