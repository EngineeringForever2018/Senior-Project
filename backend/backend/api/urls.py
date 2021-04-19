from django.urls import path, include

import backend.api.views.classroom
import backend.api.views.dummy
import backend.api.views.user
from backend.api import views
from backend.api.views.utils import error404
from rest_framework.routers import SimpleRouter

handler404 = error404

router = SimpleRouter(trailing_slash=False)

router.register(r"instructors", views.InstructorViewSet)
router.register(r"students", views.StudentViewSet)
router.register(r"classrooms", views.ClassroomViewSet)
router.register(r"instructor/classrooms", views.ClassroomViewSet)
router.register(r"assignments", views.AssignmentViewSet)


urlpatterns = [
    path(r"", include(router.urls)),
    path("joined-classrooms/<int:pk>", views.JoinedClassroomDetail.as_view()),
    path('public-dummy', views.dummy.public_dummy),
    path('private-dummy', views.dummy.private_dummy),
    path("dummies/<int:pk>", views.DummyDetail.as_view(), name="dummy-detail"),
    path("special-dummies", views.dummy.AfterDummyView.as_view(), name="dummy-list"),
    path('users', views.user.UsersView.as_view()),
    path('user', views.user.UserView.as_view()),
    path("students/<int:pk>/home", views.StudentHomeView.as_view()),
    path('instructor/classrooms/<int:classroom_pk>/assignments', views.classroom.AssignmentsView.as_view()),
    path('instructor/classrooms/<int:classroom_pk>/assignments/<int:pk>', views.classroom.AssignmentView.as_view()),
    # path('classrooms/<int:classroom_pk>/students', views.classroom.ClassroomStudentsView.as_view()),
    # path('classrooms/<int:classroom_pk>/students/<int:pk>', views.classroom.ClassroomStudentView.as_view()),
    path('student/classrooms/<int:classroom_pk>/assignments', views.classroom.StudentAssignmentsView.as_view()),
    path('student/classrooms/<int:classroom_pk>/assignments/<int:pk>', views.classroom.StudentAssignmentView.as_view()),
    path('student/classrooms/<int:classroom_pk>/assignments/<int:assignment_pk>/submissions',
         views.classroom.SubmissionsView.as_view()),
    path('student/classrooms/<int:classroom_pk>/assignments/<int:assignment_pk>/submissions/<int:pk>',
         views.classroom.SubmissionView.as_view()),
    path('instructor/classrooms/<int:classroom_pk>/assignments/<int:assignment_pk>/submissions',
         views.classroom.InstructorSubmissionsView.as_view()),
    path('instructor/classrooms/<int:classroom_pk>/assignments/<int:assignment_pk>/submissions/<int:pk>',
         views.classroom.InstructorSubmissionView.as_view()),
    path('instructor/classrooms/<int:classroom_pk>/assignments/<int:assignment_pk>/accepted-submissions',
         views.classroom.AcceptedSubmissionsView.as_view()),
    path(
        'instructor/classrooms/<int:classroom_pk>/assignments/<int:assignment_pk>/submissions/<int:submission_pk>/report',
        views.classroom.ReportView.as_view()),
    path(
        'instructor/classrooms/<int:classroom_pk>/assignments/<int:assignment_pk>/' +
        'submissions/<int:submission_pk>/detailed-report',
        views.classroom.DetailedReportView.as_view()
    ),
]
