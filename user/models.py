from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'

    base_role = Role.ADMIN

    role = models.CharField(max_length=75, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(self, *args, **kwargs)
        return results.filter(role=User.Role.STUDENT)

class Student(User):

    base_role = User.Role.STUDENT

    class Meta:
        proxy = True

    def welcome(self):
        return "only for students"

# @receiver(post_save, sender=Student)
# def create_user_profile(sender, instance, created,**kwargs):
#     if created and instance.role == "STUDENT":
#         StudentProfile.objects.create(user=instance)

    


class StudentProfile(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)

class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(self, *args, **kwargs)
        return results.filter(role=User.Role.TEACHER)

class Teacher(User):

    base_role = User.Role.TEACHER

    class Meta:
        proxy = True

    def welcome(self):
        return "only for teachers"


# @receiver(post_save, sender=Teacher)
# def create_user_profile(sender, instance, created,**kwargs):
#     if created and instance.role == "TEACHER":
#         StudentProfile.objects.create(user=instance)
        

class TeacherProfile(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True, blank=True)


