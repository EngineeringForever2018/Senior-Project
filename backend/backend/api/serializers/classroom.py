from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from backend.api.models.classroom import Classroom, Assignment, Submission
from backend.api.models.user import Student


class ClassroomSerializer(HyperlinkedModelSerializer):
    instructor = serializers.HyperlinkedRelatedField(view_name="instructor-detail", read_only=True)
    class Meta:
        model = Classroom
        fields = ['id', 'instructor', "students", "assignments", 'title']


class JoinedClassroomSerializer(ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Student.objects.all())

    class Meta:
        model = Classroom
        fields = ["id", "students"]

    def update(self, instance, validated_data):
        instance.students.add(validated_data["student"])
        return instance


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
