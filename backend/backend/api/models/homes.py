from django.db import models
from django.db.models import Model
from django.db.models import CASCADE


class StudentHome(Model):
    @property
    def classrooms(self):
        return self.student.classrooms
