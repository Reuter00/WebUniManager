from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


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


# Creates automaticly a user for loggin when creating a new Student
@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # User name is a combination of the first latter of the first name and the last name
        name = instance.name
        firstname = name.split()[0]
        lastname = name.split()[1]
        shoppedusername = firstname[0] + name.split()[1]
        User.objects.create(username=shoppedusername.lower(), password=shoppedusername.lower(), first_name=firstname,
                            last_name=lastname, is_staff=False, email=instance.email, is_active=True, is_student=True,
                            is_teacher=False)


post_save.connect(create_user_profile, sender=Student)


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


# Creates automaticly a user for loggin when creating a new Student
@receiver(post_save, sender=Professor)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # User name is a combination of the first latter of the first name and the last name
        name = instance.name
        firstname = name.split()[0]
        lastname = name.split()[1]
        shoppedusername = firstname[0] + name.split()[1]
        User.objects.create(username=shoppedusername.lower(), password=shoppedusername.lower(), first_name=firstname,
                            last_name=lastname, is_staff=False, email=instance.email, is_active=True, is_student=False,
                            is_teacher=True)


post_save.connect(create_user_profile, sender=Professor)


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
