from django.contrib.auth.models import AbstractUser

# Quick reference: https://docs.djangoproject.com/en/3.1/topics/db/models/

# Create your models here.


from backend.api.models.user import User, Instructor, Student
from backend.api.models.classroom import Classroom, Assignment, Submission
from backend.api.models.dummy import Dummy, AfterDummy
