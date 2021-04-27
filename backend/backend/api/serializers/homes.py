from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from backend.api.models import Student, Classroom, Assignment
from backend.api.serializers import AssignmentSerializer


class StudentHomeSerializer(serializers.ModelSerializer):
    #assignments = serializers.PrimaryKeyRelatedField(source = 'classrooms.assignments', queryset = Assignment.objects.all())
    assignments = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['classrooms', 'assignments', 'id']
    def get_assignments(self,obj):
        queryassignments = Assignment.objects.filter(classroom__in = obj.classrooms.all())
        return AssignmentSerializer(queryassignments, many = True).data
