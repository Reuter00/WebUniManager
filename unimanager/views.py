from django.shortcuts import render
from unimanager.models import *
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseRedirect


def myarea(request):
    userid = None
    schoolyears = SchoolYear.objects.all()

    if request.user.is_authenticated:
        userid = request.user.id
        isstudentorprofessor = request.user.is_student

        if isstudentorprofessor:
            studentinfo = Student.objects.get(student_user_id=userid)
            studentsubjects = StudentSubject.objects.filter(student=studentinfo)
            context = {
                'info': studentinfo,
                'subjects': studentsubjects,
                'schoolyears': schoolyears,
            }

        else:
            professorinfo = Professor.objects.get(teacher_user_id=userid)
            professorsubjects = ProfessorSubject.objects.filter(professor=professorinfo)
            context = {
                'info': professorinfo,
                'subjects': professorsubjects,
                'schoolyears': schoolyears,
            }

    else:  # Redirect to login if not logged in
        return HttpResponseRedirect('/login/')

    return render(request, 'unimanager/myarea.html', context)


# Logout View
def logout_view(request):
    logout(request)
