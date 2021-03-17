from django.urls import path

import backend.api.views.classroom
import backend.api.views.dummy
import backend.api.views.user
from backend.api import views
from backend.api.views.utils import error404

handler404 = error404

urlpatterns = [
    path('public-dummy', views.dummy.public_dummy),
    path('private-dummy', views.dummy.private_dummy),
    path('users', views.user.UsersView.as_view()),
    path('user', views.user.UserView.as_view()),
    path('instructor/classrooms', views.classroom.ClassroomsView.as_view()),
    path('instructor/classrooms/<int:pk>', views.classroom.ClassroomView.as_view()),
    path('instructor/classrooms/<int:classroom_pk>/assignments', views.classroom.AssignmentsView.as_view()),
    path('instructor/classrooms/<int:classroom_pk>/assignments/<int:pk>', views.classroom.AssignmentView.as_view()),
    path('classrooms/<int:classroom_pk>/students', views.classroom.ClassroomStudentsView.as_view()),
    path('classrooms/<int:classroom_pk>/students/<int:pk>', views.classroom.ClassroomStudentView.as_view()),
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
