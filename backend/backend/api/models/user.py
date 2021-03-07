from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Convenience method for creating users correctly
    @classmethod
    def create(cls, user_type='student', *args, **kwargs):
        if user_type == 'student':
            user = cls.objects.create(is_student=True, is_instructor=False, *args, **kwargs)
            Student.objects.create(user=user)

            return user
        else:
            user = cls.objects.create(is_student=False, is_instructor=True, *args, **kwargs)
            Instructor.objects.create(user=user)

            return user

    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)

    def user_type(self):
        if self.is_student:
            return 'student'
        else:
            return 'instructor'

    def __str__(self):
        return self.username


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username