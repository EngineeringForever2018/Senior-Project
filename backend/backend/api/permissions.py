from rest_framework.permissions import BasePermission, SAFE_METHODS

from backend.api.models import Classroom, Assignment


class IsClaimedInstructor(BasePermission):
    """
    Allows an instructor access to a resource as long as they are who they claim.
    """

    def has_permission(self, request, view):
        claimed_id = request.data["instructor"]
        if claimed_id is not None:
            user = request.user
            return user.role == "instructor" and user.instructor.id == claimed_id

        return True


class IsClassInstructorOrReadOnly(BasePermission):
    """
    Allows the instructor of a classroom to modify it, and other users may read it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return user.role == "instructor" and obj.instructor == user.instructor


class IsClassMember(BasePermission):
    """
    Allows members of the class to access it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        is_student = user.role == "student" and user.student in obj.students
        is_instructor = user.role == "instructor" and user.instructor == obj.instructor

        return is_student or is_instructor


class AssociatedWithInstructor(BasePermission):
    """
    Allows students who belong to a class from this instructor to view them, or the
    instructor themselves.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "student":
            student_associated = Classroom.objects.filter(instructor=obj.id, students=user.student).count() > 0

        instructor_associated = user.role == "instructor" and user.instructor == obj

        return instructor_associated or student_associated


class AssociatedWithStudent(BasePermission):
    """
    Allows instructors or students who share a class with this student to view them, or
    the student themselves.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "instructor":
            instructor_associated = Classroom.objects.filter(instructor=user.instructor, students=obj).count() > 0

        student_associated = user.role == "student" and (obj == user.student or Classroom.objects.filter(students=[user.student, obj]).count() > 0)

        return student_associated or instructor_associated


class IsStudent(BasePermission):
    """
    True for students.
    """

    def has_permission(self, request, view):
        return request.user.role == "student"


class IsAssignmentStudent(BasePermission):
    """
    True if this assignment belongs to one of the student's classes.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "student":
            return Assignment.objects.filter(id=obj.id, classroom__in=user.student.classrooms.all()).count() > 0

        return True


class IsAssignmentInstructorOrReadOnly(BasePermission):
    """
    Allows instructors to edit their assignments, but students can only read them.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        return user.role == "instructor" and obj.classroom.instructor == user.instructor
