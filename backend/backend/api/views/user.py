from django.http import JsonResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.api import utils
from backend.api.models import User, Instructor, Student, Classroom
from backend.api.serializers import InstructorSerializer, StudentSerializer
from backend.api.permissions import AssociatedWithInstructor, AssociatedWithStudent
from backend.api.utils import location


class IncorrectUserType(APIException):
    status_code = 400
    default_detail = "Wrong user type for resource."
    default_code = "incorrect_user_type"

    def __init__(self, user_type, expected_type):
        self.detail = self.default_detail + f" Expected: {expected_type}. Got: {user_type}."


@permission_classes([AllowAny])
class UsersView(APIView):
    # Note: If there is ever a bug about these methods not having a format parameter add a 'format=None' parameter.
    @permission_classes([AllowAny])
    def post(self, request):
        username = utils.jwt_get_username_from_payload_handler(utils.jwt_decode_token(request.data['token']))
        data = request.data
        user_type, first_name, last_name = (data['type'], data['first_name'], data['last_name'])

        User.create(username=username, first_name=first_name, last_name=last_name, user_type=user_type)

        response_data = request.data
        response_data['username'] = username

        response = JsonResponse(response_data)
        response['Location'] = location(request, f'/users/{username}')
        response.status_code = status.HTTP_201_CREATED

        return response


class UserView(APIView):
    @staticmethod
    def get(request):
        user = request.user
        username, user_type, first_name, last_name = user.username, user.user_type(), user.first_name, user.last_name

        return Response(
            {'username': username, 'user_type': user_type, 'first_name': first_name, 'last_name': last_name})


class InstructorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    permission_classes = [IsAuthenticated, AssociatedWithInstructor]

    def get_queryset(self):
        user = self.request.user

        if user.role == "student":
            return Instructor.objects.filter(classroom__in=user.student.classrooms.all())
        else:
            return Instructor.objects.filter(id=user.instructor.id)


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = [IsAuthenticated, AssociatedWithStudent]

    def get_queryset(self):
        user = self.request.user

        if user.role == "student":
            classrooms = user.student.classrooms.all()
        else:
            classrooms = Classroom.objects.filter(instructor=user.instructor)

        return Student.objects.filter(classrooms__in=classrooms).distinct()
