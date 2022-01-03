from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)


class Semester(models.Model):
    number = models.CharField(max_length=2)
    start = models.DateField(blank=True)
    end = models.DateField(blank=True)

    def __str__(self):
        return self.number


class SchoolYear(models.Model):
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.year


class CoursesType(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Courses(models.Model):
    name = models.CharField(max_length=25)
    type = models.ForeignKey(CoursesType, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{} | {}'.format(self.type, self.name)


class Subject(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    number = models.CharField(max_length=250)

    def __str__(self):
        return self.number


class Student(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True)
    student_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    # student_profile_pic = models.ImageField(upload_to="classroom/student_profile_pic", blank=True)

    def __str__(self):
        return self.name


# Creates automaticly a user for loggin when creating a new Student
@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # User name is a combination of the first latter of the first name and the last name
        name = instance.name
        firstname = name.split()[0]
        lastname = name.split()[1]
        shoppedusername = firstname[0] + name.split()[1]
        newuser = User.objects.create(is_superuser=True, username=shoppedusername.lower(),
                                      first_name=firstname,
                                      last_name=lastname, is_staff=False, email=instance.email, is_active=True,
                                      is_student=True,
                                      is_teacher=False)
        # uses User set_password for encrypting password
        newuser.set_password(shoppedusername.lower())
        newuser.save()


post_save.connect(create_user_profile, sender=Student)


# To make sure that the last Student created gets the last User id in student_user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    lateststudent = Student.objects.latest('id')
    if created and instance.first_name + ' ' + instance.last_name == lateststudent.name:
        lateststuser = User.objects.latest('id')
        lateststudent.student_user = lateststuser
        lateststudent.save()


post_save.connect(create_user_profile, sender=User)


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, default=1, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1, blank=True, null=True)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.student, self.subject, self.classroom, self.schoolyear, self.semester)


class Professor(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.IntegerField()
    teacher_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    # teacher_profile_pic = models.ImageField(upload_to="classroom/teacher_profile_pic", blank=True)

    def __str__(self):
        return self.name


# Creates automaticly a user for loggin when creating a new Student
@receiver(post_save, sender=Professor)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # User name is a combination of the first latter of the first name and the last name
        name = instance.name
        firstname = name.split()[0]
        lastname = name.split()[1]
        shoppedusername = firstname[0] + name.split()[1]
        newuser = User.objects.create(is_superuser=True, username=shoppedusername.lower(),
                                      first_name=firstname,
                                      last_name=lastname, is_staff=False, email=instance.email, is_active=True,
                                      is_student=False,
                                      is_teacher=True)
        # uses User set_password for encrypting password
        newuser.set_password(shoppedusername.lower())
        newuser.save()


post_save.connect(create_user_profile, sender=Professor)


# To make sure that the last Professor created gets the last User id in teacher_user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        latestprofessor = Professor.objects.latest('id')
        lateststuser = User.objects.latest('id')
        latestprofessor.teacher_user = lateststuser
        latestprofessor.save()


post_save.connect(create_user_profile, sender=User)


class ProfessorSubject(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, default=1, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1, blank=True, null=True)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.professor, self.subject, self.classroom, self.schoolyear, self.semester)


class SPRelation(models.Model):
    professor = models.ForeignKey(ProfessorSubject, related_name='professors', on_delete=models.CASCADE)
    student = models.ForeignKey(StudentSubject, related_name='students', on_delete=models.CASCADE)
    mark = models.IntegerField(validators=[MaxValueValidator(20)], null=True)

    def __str__(self):
        return '{} | {} | {} '.format(self.professor, self.student, self.mark)
