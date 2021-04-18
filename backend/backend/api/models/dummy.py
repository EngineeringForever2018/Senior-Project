from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models
from django.db.models import CASCADE, Model
from notebooks import StyleProfile


class Dummy(Model):
    is_dummy = models.BooleanField(default=True)


class AfterDummy(Model):
    dummy = models.OneToOneField(Dummy, on_delete=CASCADE)


def create_after_dummy(instance, created, raw, **kwargs):
    if not created or raw:
        return

    AfterDummy.objects.create(dummy=instance)


models.signals.post_save.connect(create_after_dummy, sender=Dummy)
