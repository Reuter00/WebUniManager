from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Classroom)
admin.site.register(Professor)
admin.site.register(SPRelation)
admin.site.register(StudentSubject)
admin.site.register(ProfessorSubject)
admin.site.register(SchoolYear)
admin.site.register(Semester)
admin.site.register(Courses)
admin.site.register(CoursesType)
