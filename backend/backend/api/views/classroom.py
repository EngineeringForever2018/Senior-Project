from datetime import datetime

import pytz
from django.http import Http404, FileResponse, HttpResponse
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import os

from backend.api.models.classroom import Classroom, Assignment, Submission
from backend.api.models.essay import Essay
from backend.api.models.user import Instructor, Student, User
from backend.api.serializers import JoinedClassroomSerializer
from backend.api.serializers.classroom import ClassroomSerializer, ClassroomStudentSerializer, AssignmentSerializer, \
    SubmissionSerializer
from backend.api.utils import location
from backend.api.views.utils import verify_user_type, post_serialize, put_serialize
from backend.api.permissions import IsClassMember, IsClaimedInstructor, IsClassInstructorOrReadOnly, IsStudent, IsAssignmentStudent, IsAssignmentInstructorOrReadOnly
from notebooks import TextProcessor
from backend.api.models.classroom import document_text
from io import BytesIO
from django.core.files import File
from docx import Document
from notebooks import StyleProfile, PreprocessedText
import mimetypes


# TODO: (Refactoring) Learn how to use query sets and see if that cleans up any of this code.

def download_file(request):
    # fill these variables with real values
    fl_path = '1.docx'
    filename = '1.docx'

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsClassMember, IsClassInstructorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.role == "student":
            return Classroom.objects.filter(students=user.student)
        else:
            return Classroom.objects.filter(instructor=user.instructor)

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user.instructor)


class JoinedClassroomDetail(generics.UpdateAPIView):
    lookup_field = "pk"
    queryset = Classroom.objects.all()
    serializer_class = JoinedClassroomSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_update(self, serializer):
        serializer.save(student=self.request.user.student)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsAssignmentStudent, IsAssignmentInstructorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user.role == "student":
            classrooms = user.student.classrooms.all()
        else:
            classrooms = Classroom.objects.filter(instructor=user.instructor)

        return Assignment.objects.filter(classroom__in=classrooms)


class ClassroomsView(APIView):
    """
    List classrooms or create a new one.
    """
    @staticmethod
    def post(request):
        """Create a new classroom for the user who made this request."""
        verify_user_type(request, 'instructor')

        request.data['instructor'] = Instructor.objects.get(user=request.user).id
        serializer = post_serialize(request, ClassroomSerializer)
        classroom = serializer.save()

        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response['Location'] = location(request, f'/instructor/classrooms/{classroom.id}')

        return response

    @staticmethod
    def get(request):
        """Return a list of all classrooms for the instructor who made this request."""
        verify_user_type(request, "instructor")

        instructor = Instructor.objects.get(user=request.user)
        classrooms = Classroom.objects.filter(instructor=instructor)

        serializer = ClassroomSerializer(classrooms, many=True)

        return Response(serializer.data)


class ClassroomView(APIView):
    """
    Retrieve, update, or delete a classroom.
    """
    def get(self, request, pk):
        """Retrieve the classroom specified by the instructor."""
        verify_user_type(request, "instructor")

        classroom = self.get_object(request, pk)
        serializer = ClassroomSerializer(classroom, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        """Update the classroom specified by the instructor."""
        verify_user_type(request, "instructor")

        classroom = self.get_object(request, pk)
        request.data['instructor'] = Instructor.objects.get(user=request.user).id
        serializer = put_serialize(request, classroom, ClassroomSerializer)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        """Delete the classroom specified by the instructor."""
        verify_user_type(request, "instructor")

        classroom = self.get_object(request, pk)
        serializer = ClassroomSerializer(classroom)
        # Getting the serializer data before the classroom has been deleted allows id to be included.
        data = serializer.data

        classroom.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(request, pk):
        try:
            # We only want to return this classroom if it belongs to this instructor.
            instructor = Instructor.objects.get(user=request.user)

            return Classroom.objects.get(instructor=instructor, id=pk)
        except Classroom.DoesNotExist:
            raise Http404


class ClassroomStudentsView(APIView):
    """
    Join a classroom as a student or view the students in a classroom as either role.
    """
    @staticmethod
    def post(request, classroom_pk):
        """Join this classroom as a student."""
        verify_user_type(request, 'student')

        classroom = Classroom.objects.get(id=classroom_pk)
        student = Student.objects.get(user=request.user)

        classroom.students.add(student)
        classroom.save()

        serializer = ClassroomStudentSerializer(student)

        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response['Location'] = location(request, f'/student/classrooms/{classroom.id}')

        return response

    def get(self, request, classroom_pk):
        """View the students within the classroom as either a student in this class or its instructor."""
        classroom = self.get_object(classroom_pk)

        self.validate_user(classroom, request)

        students = Student.objects.filter(classroom=classroom)
        serializer = ClassroomStudentSerializer(students, many=True)

        return Response(serializer.data)

    @staticmethod
    def validate_user(classroom, request):
        if verify_user_type(request, 'student', no_except=True):
            ClassroomStudentsView.assert_valid_student(request, classroom)
        else:
            ClassroomStudentsView.assert_correct_instructor(request, classroom)

    @staticmethod
    def get_object(classroom_pk):
        return Classroom.objects.get(id=classroom_pk)

    @staticmethod
    def assert_correct_instructor(request, classroom):
        try:
            instructor = Instructor.objects.get(user=request.user)
            Classroom.objects.get(id=classroom.id, instructor=instructor)
        except Classroom.DoesNotExist:
            raise PermissionDenied(detail="Instructor does not own this classroom.")

    @staticmethod
    def assert_valid_student(request, classroom):
        try:
            student = Student.objects.get(user=request.user)
            Classroom.objects.get(id=classroom.id, students=student)
        except Classroom.DoesNotExist:
            raise PermissionDenied(detail="Student is not within this classroom.")


class ClassroomStudentView(APIView):
    """
    View a specific student in this class as either role or remove a student from the class as an instructor.
    """
    @staticmethod
    def get_object(classroom, pk):
        try:
            return Student.objects.get(classroom=classroom, id=pk)
        except Student.DoesNotExist:
            raise NotFound(detail="Student does not belong to this classroom.")

    def get(self, request, classroom_pk, pk):
        """View a specific student within this class."""
        classroom = ClassroomStudentsView.get_object(classroom_pk)

        ClassroomStudentsView.validate_user(classroom, request)

        student = self.get_object(classroom, pk)
        serializer = ClassroomStudentSerializer(student)

        student_user = User.objects.get(student=student)

        data = serializer.data
        data['first_name'] = student_user.first_name
        data['last_name'] = student_user.last_name

        return Response(data)

    def delete(self, request, classroom_pk, pk):
        """Remove a student from this class as an instructor."""
        classroom = ClassroomStudentsView.get_object(classroom_pk)

        ClassroomStudentsView.validate_user(classroom, request)
        verify_user_type(request, 'instructor')

        student = self.get_object(classroom, pk)
        serializer = ClassroomStudentSerializer(student)
        data = serializer.data

        classroom.students.remove(student)
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class AssignmentsView(APIView):
    """
    Add an assignment or view a list of all assignments in this classroom.
    """
    def post(self, request, classroom_pk):
        """Add an assignment to this classroom."""
        verify_user_type(request, 'instructor')

        request.data['classroom'] = classroom_pk
        request.data['due_date'] = self.date_decode(request.data['due_date'])

        serializer = post_serialize(request, AssignmentSerializer)
        assignment = serializer.save()

        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response['Location'] = location(request, f'/instructor/classrooms/{classroom_pk}/assignments/{assignment.id}')

        return response

    @staticmethod
    def get(request, classroom_pk):
        """View all the assignments within this classroom."""
        verify_user_type(request, 'instructor')

        # TODO: (Refactoring) See if query sets can allow this to be done by only querying assignments.
        # TODO: (Bug) Return 400 level errors when instructors/classrooms are not found.
        instructor = Instructor.objects.get(user=request.user)
        classroom = Classroom.objects.get(instructor=instructor, id=classroom_pk)
        assignments = Assignment.objects.filter(classroom=classroom)
        serializer = AssignmentSerializer(assignments, many=True)

        return Response(serializer.data)

    @staticmethod
    def date_decode(due_date):
        year, month, day, hour, minute = (
            due_date['year'], due_date['month'], due_date['day'], due_date['hour'], due_date['minute'])

        return datetime(year, month, day, hour, minute, second=59, tzinfo=pytz.UTC)


class AssignmentView(APIView):
    """Retrieve, update, or delete an assignment."""
    def get(self, request, classroom_pk, pk):
        """View a specific assignment."""
        verify_user_type(request, 'instructor')

        assignment = self.get_object(request, classroom_pk, pk)
        serializer = AssignmentSerializer(assignment)

        return Response(serializer.data)

    def put(self, request, classroom_pk, pk):
        """Update an assignment."""
        verify_user_type(request, 'instructor')

        assignment = self.get_object(request, classroom_pk, pk)
        request.data['classroom'] = classroom_pk
        request.data['due_date'] = AssignmentsView.date_decode(request.data['due_date'])
        serializer = put_serialize(request, assignment, AssignmentSerializer)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, classroom_pk, pk):
        """Delete an assignment."""
        verify_user_type(request, 'instructor')

        assignment = self.get_object(request, classroom_pk, pk)
        serializer = AssignmentSerializer(assignment)
        data = serializer.data

        assignment.delete()

        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(request, classroom_pk, pk):
        try:
            # Don't return the assignment if this instructor does not own this class.
            instructor = Instructor.objects.get(user=request.user)
            classroom = Classroom.objects.get(instructor=instructor, id=classroom_pk)

            return Assignment.objects.get(classroom=classroom, id=pk)
        except Assignment.DoesNotExist:
            raise NotFound(detail='Assignment does not exist.')


class StudentAssignmentsView(APIView):
    """View the assignments within the classroom."""
    @staticmethod
    def get(request, classroom_pk):
        """View a list of the assignments in this class."""
        verify_user_type(request, 'student')

        # TODO: (Bug) This isn't checking whether the student is within the class.
        assignments = Assignment.objects.filter(classroom=classroom_pk)
        serializer = AssignmentSerializer(assignments, many=True)

        return Response(serializer.data)


class StudentAssignmentView(APIView):
    """View an assignment within this classroom."""
    def get(self, request, classroom_pk, pk):
        """Get an assignment for this classroom."""
        verify_user_type(request, 'student')

        assignment = self.get_object(request, classroom_pk, pk)
        serializer = AssignmentSerializer(assignment)

        return Response(serializer.data)

    @staticmethod
    def get_object(request, classroom_pk, pk):
        # TODO: (Bug) This does not check if the student is within the classroom.
        try:
            return Assignment.objects.get(classroom=classroom_pk, id=pk)
        except Assignment.DoesNotExist:
            raise NotFound(detail='Assignment does not exist.')


class SubmissionsView(APIView):
    """
    Post a submission or view previously posted submissions.
    """
    parser_classes = (MultiPartParser, FormParser,)
    i = 0

    @classmethod
    def post(cls, request, classroom_pk, assignment_pk):
        """Post a submission for this assignment."""
        verify_user_type(request, 'student')
        processor = TextProcessor()

        # TODO: (Bug) Check that assignment and student are valid.
        student = Student.objects.get(user=request.user)

        doc = Document(request.data["file"]) 
        preprocessed_text = processor(document_text(doc))

        # RECAP: (Bug) Django says file is empty here. When seeking to 0, saved files
        #        have no content
        f = open(f"{student.user.id}-submission-{cls.i}.nb", "wb+")
        cls.i += 1
        f.write(preprocessed_text.binary.read())
        f.seek(0)
        request.data["file"] = File(f)
        request.data['assignment'] = assignment_pk
        request.data['student'] = student.id
        request.data['date'] = datetime.now(tz=pytz.UTC)

        serializer = post_serialize(request, SubmissionSerializer)
        submission = serializer.save()

        response = Response({'date': submission.date, 'id': submission.id}, status=status.HTTP_201_CREATED)
        resource_path = f'/student/classrooms/{classroom_pk}/assignments/{assignment_pk}/submissions/{submission.id}'
        response['Location'] = location(request, resource_path)

        return response

    @staticmethod
    def get(request, classroom_pk, assignment_pk):
        """View previous submissions."""
        verify_user_type(request, 'student')

        # TODO: (Bug) Error check path
        student = Student.objects.get(user=request.user)
        submissions = Submission.objects.filter(student=student, assignment=assignment_pk)

        serializer = SubmissionSerializer(submissions, many=True)

        return Response(serializer.data)


class SubmissionView(APIView):
    """
    View a specific submission.
    """
    def get(self, request, classroom_pk, assignment_pk, pk):
        """Retrieve a submission."""
        verify_user_type(request, 'student')

        submission = self.get_object(request, classroom_pk, assignment_pk, pk)
        serializer = SubmissionSerializer(submission)

        return Response(serializer.data)

    @staticmethod
    def get_object(request, classroom_pk, assignment_pk, pk):
        # TODO: (Bug) make sure student is within class.
        try:
            assignment = Assignment.objects.get(classroom=classroom_pk, id=assignment_pk)
            return Submission.objects.get(assignment=assignment, id=pk)
        except not Submission.DoesNotExist:
            return NotFound(detail='Submission does not exist.')


class InstructorSubmissionsView(APIView):
    """
    Student submissions from the instructors point of view.
    """
    @staticmethod
    def get(request, classroom_pk, assignment_pk):
        """View all submissions for this assignment."""
        verify_user_type(request, 'instructor')

        instructor = Instructor.objects.get(user=request.user)
        classroom = Classroom.objects.get(instructor=instructor, id=classroom_pk)
        assignment = Assignment.objects.get(classroom=classroom, id=assignment_pk)

        submissions = Submission.objects.filter(assignment=assignment)

        serializer = SubmissionSerializer(submissions, many=True)

        return Response(serializer.data)


class InstructorSubmissionView(APIView):
    """
    Individual submissions from the instructor's point of view.
    """
    def get(self, request, classroom_pk, assignment_pk, pk):
        """Retrieve a submission for the instructor"""
        verify_user_type(request, 'instructor')

        submission = self.get_object(request, classroom_pk, assignment_pk, pk)
        serializer = SubmissionSerializer(submission)

        return Response(serializer.data)

    @staticmethod
    def get_object(request, classroom_pk, assignment_pk, pk):
        try:
            instructor = Instructor.objects.get(user=request.user)
            classroom = Classroom.objects.get(instructor=instructor, id=classroom_pk)
            assignment = Assignment.objects.get(classroom=classroom, id=assignment_pk)

            return Submission.objects.get(assignment=assignment, id=pk)
        except Submission.DoesNotExist:
            return NotFound(detail='Submission does not exist.')


class AcceptedSubmissionsView(APIView):
    """
    Accept submissions.
    """
    @staticmethod
    def post(request, classroom_pk, assignment_pk):
        """Accept a submission as an instructor."""
        verify_user_type(request, 'instructor')

        submission_pk = request.data['id']

        classroom = Classroom.objects.get(id=classroom_pk)
        assignment = Assignment.objects.get(classroom=classroom, id=assignment_pk)
        submission = Submission.objects.get(assignment=assignment, id=submission_pk)

        profile = StyleProfile(BytesIO(submission.student.profile.file.read()))

        profile.feed(PreprocessedText(BytesIO(submission.file.read())))

        newfilename = f"{submission.student.user.id}-profile.nb"
        submission.student.profile.save(newfilename, BytesIO(profile.binary.read()))

        submission.student.save()

        response = Response({}, status=status.HTTP_201_CREATED)
        # response['Location'] = location(request, f'/student/essays/{essay.id}')

        return response


class ReportView(APIView):
    """Get contrast reports for submissions."""
    @staticmethod
    def get(request, classroom_pk, assignment_pk, submission_pk):
        """Retrieve contrast report."""
        verify_user_type(request, 'instructor')

        classroom = Classroom.objects.get(id=classroom_pk)
        assignment = Assignment.objects.get(classroom=classroom, id=assignment_pk)
        submission = Submission.objects.get(assignment=assignment, id=submission_pk)

        response = Response(submission.contrast_report())

        return response


class DetailedReportView(APIView):
    @staticmethod
    def get(request, classroom_pk, assignment_pk, submission_pk):
        verify_user_type(request, 'instructor')

        classroom = Classroom.objects.get(id=classroom_pk)
        assignment = Assignment.objects.get(classroom=classroom, id=assignment_pk)
        submission = Submission.objects.get(assignment=assignment, id=submission_pk)

        # wf = open('dummy-detailed-report.docx', 'rb')
        # response = Response({'file': wf}, content_type='Multipart/Form-data')
        # response = FileResponse(wf, content_type='docx')
        # response['Content-Length'] = len(wf.read())
        # response['Content-Length'] = os.fstat(wf.fileno()).st_size
        # response['Content-Disposition'] = f'attachment; filename="dummy-detailed-report.docx"'
        # file_path = os.path.join(settings.MEDIA_ROOT, path)
        # if os.path.exists(file_path):
        with open('dummy-detailed-report.docx', 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/docx")
            response['Content-Disposition'] = 'inline; filename=' + "dummy-detailed-report.docx"
            return response
