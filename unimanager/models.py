from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)


class SchoolYear(models.Model):
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.year


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
    student_user = models.ForeignKey(User, on_delete=models.CASCADE)

    # student_profile_pic = models.ImageField(upload_to="classroom/student_profile_pic", blank=True)

    def __str__(self):
        return self.name


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return '{} {} {} {}'.format(self.student, self.subject, self.classroom, self.schoolyear)


class Professor(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.IntegerField()
    teacher_user = models.ForeignKey(User, on_delete=models.CASCADE)

    # teacher_profile_pic = models.ImageField(upload_to="classroom/teacher_profile_pic", blank=True)

    def __str__(self):
        return self.name


class ProfessorSubject(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return '{} {} {} {}'.format(self.professor, self.subject, self.classroom, self.schoolyear)


class SPRelation(models.Model):
    professor = models.ForeignKey(Professor, related_name='professors', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='subjects', on_delete=models.CASCADE)
    mark = models.IntegerField(null=True)

    def __str__(self):
        return self.professor, self.student, self.subject, self.mark
