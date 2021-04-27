from rest_framework.generics import RetrieveAPIView
from backend.api.models import Student
from backend.api.serializers.homes import StudentHomeSerializer


class StudentHomeView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentHomeSerializer

    def get_object(self):
        pk = self.request.user.student.id
        return self.queryset.get(id=pk)
