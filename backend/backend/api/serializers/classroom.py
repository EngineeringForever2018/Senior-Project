from rest_framework import serializers

from backend.api.models.classroom import Classroom, Assignment, Submission
from backend.api.models.user import Student


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'instructor', 'title']


class ClassroomStudentSerializer(serializers.ModelSerializer):
    """
    Serializer for students viewed under /classrooms/{id}/students
    """
    class Meta:
        model = Student
        fields = ['id']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'classroom', 'title', 'description', 'due_date']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'date', 'file']
