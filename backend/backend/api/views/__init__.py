# Create your views here.

# Quick reference: https://www.django-rest-framework.org/api-guide/views/

# These views are here to quickly check if the api is working.

from backend.api.views.dummy import DummyDetail
from backend.api.views.home import StudentHomeView
from backend.api.views.user import InstructorViewSet, StudentViewSet
from backend.api.views.classroom import ClassroomViewSet, JoinedClassroomDetail, AssignmentViewSet
