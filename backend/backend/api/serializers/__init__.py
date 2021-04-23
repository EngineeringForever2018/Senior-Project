from django.contrib.auth.models import Group
from rest_framework import serializers

from backend.api.serializers.user import InstructorSerializer, StudentSerializer
from backend.api.serializers.classroom import JoinedClassroomSerializer


# Quick reference: https://www.django-rest-framework.org/api-guide/serializers/


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
