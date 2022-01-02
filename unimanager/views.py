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

    # Variable for School year and semester
    schoolyears = SchoolYear.objects.all().order_by('-year')
    selected_schoolyear_info = SchoolYear.objects.get(year=selected_schoolyear)
    semesters = Semester.objects.all()

    # Check if loged in user is a student or a professor
    if request.user.is_authenticated:
        userid = request.user.id
        isstudentorprofessor = request.user.is_student

        if isstudentorprofessor:
            studentinfo = Student.objects.get(student_user_id=userid)
            studentsubjects = StudentSubject.objects.filter(student=studentinfo, schoolyear=selected_schoolyear_info.id)
            context = {
                'info': studentinfo,
                'subjects': studentsubjects,
                'currentschoolyears': selected_schoolyear_info,
                'schoolyears': schoolyears,
                'semesters': semesters,

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

    else:  # Redirect to login if not logged in
        return HttpResponseRedirect('/login/')

    return render(request, 'unimanager/myarea.html', context)


# Logout View
def logout_view(request):
    logout(request)
