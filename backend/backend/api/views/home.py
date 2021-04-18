from rest_framework.generics import RetrieveAPIView
from backend.api.models import Student
from backend.api.serializers.homes import StudentHomeSerializer


class StudentHomeView(RetrieveAPIView):
    lookup_field = "pk"
    queryset = Student.objects.all()
    serializer_class = StudentHomeSerializer
