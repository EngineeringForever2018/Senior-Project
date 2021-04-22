from django.contrib.auth.models import AbstractUser

# Quick reference: https://docs.djangoproject.com/en/3.1/topics/db/models/

# Create your models here.


from backend.api.models.essay import Essay
from backend.api.models.classroom import Classroom, Assignment
from backend.api.models.user import User, Student, Instructor
from backend.api.models.dummy import Dummy, AfterDummy
