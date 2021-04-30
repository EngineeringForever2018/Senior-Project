from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models

from backend.api.models.fields import NBField
from notebooks import StyleProfile


class User(AbstractUser):
    @classmethod
    def create(cls, user_type="student", *args, **kwargs):
        is_student = user_type == "student"
        is_instructor = user_type != "student"

        return cls.objects.create(is_student=is_student, is_instructor=is_instructor, *args, **kwargs)
    # @classmethod
    # def create(cls, user_type='student', *args, **kwargs):
    #     if user_type == 'student':
    #         user = cls.objects.create(is_student=True, is_instructor=False, *args, **kwargs)
    #         f = open(f"{user.id}-profile.nb", "wb+")
    #         f.write(StyleProfile().binary.read())
    #         profile=File(f)
    #         home = StudentHome.objects.create()
    #         Student.objects.create(user=user, profile=profile, home=home)

    #         return user
    #     else:
    #         user = cls.objects.create(is_student=False, is_instructor=True, *args, **kwargs)
    #         Instructor.objects.create(user=user)

    #         return user

    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)

    def user_type(self):
        if self.is_student:
            return 'student'
        else:
            return 'instructor'

    @property
    def role(self):
        return self.user_type()

    def __str__(self):
        return self.username


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile = NBField()

    def __str__(self):
        return self.user.username


def post_user_create(instance, created, raw, **kwargs):
    if instance.user_type() == "student":
        profile = StyleProfile()
        Student.objects.create(user=instance, profile=profile)
    else:
        Instructor.objects.create(user=instance)


models.signals.post_save.connect(post_user_create, sender=User)
