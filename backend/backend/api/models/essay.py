from django.db import models

from backend.api.models import Student


class Essay(models.Model):
    # Each essay has only one student who owns it. Therefore there is a many-to-one relationship between essays and
    # students. Hence we use a ForeignKey.
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # The actual file for the essay.
    file = models.FileField()
