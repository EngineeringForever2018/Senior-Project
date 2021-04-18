from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from backend.api.models import Student, Classroom


class StudentHomeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = [ "classrooms" ]
