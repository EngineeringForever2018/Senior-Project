from django.db import models
from docx import Document

from backend.api.models.user import Instructor, Student
from backend.api.models.essay import Essay
from backend.api.models.fields import NBField
from backend.api.utils import make_docx
from notebooks import StyleProfile, PreprocessedText, TextProcessor
from io import BytesIO


class Classroom(models.Model):
    # Instructors can have many classrooms. Classrooms can have only one instructor.
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    # Classrooms can have many students. Students can be enrolled in many classrooms.
    students = models.ManyToManyField(Student, related_name="classrooms")

    title = models.CharField(max_length=30)


class Assignment(models.Model):
    # Classrooms can have many assignments. Assignments can only belong to one classroom.
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="assignments")

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    due_date = models.DateTimeField()


class Submission(models.Model):
    # Students can post many submissions to an assignment. Submissions can only be posted to one assignment.
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    # Students can post many submissions. Each submission belongs to only one student.
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    date = models.DateTimeField()
    file = models.FileField()
    title = models.CharField(max_length=50)

    # TODO: Override save so that preprocessed_text is automatically generated from
    #       docx_file.
    docx_file = models.FileField()
    preprocessed_text = NBField()

    processor = TextProcessor()

    def save(self, *args, **kwargs):
        document = Document(self.docx_file)
        self.preprocessed_text = self.processor(document_text(document))

        super(Submission, self).save(*args, **kwargs)

    def contrast_report(self):
        """Generate the contrast report for this submission."""
        style_profile = self.student.profile

        # Score this submission based on the style profile.
        authorship_probability = style_profile.score(self.preprocessed_text)
        flag = style_profile.flag(self.preprocessed_text)

        return {'authorship_probability': authorship_probability, 'flag': flag}

    def detailed_report(self):
        """Generate the contrast report for this submission."""
        style_profile = self.student.profile

        # Score this submission based on the style profile.
        detailed = style_profile.detailed(self.preprocessed_text)
        return make_docx(*detailed)

    def preprocessed(self):
        return self.preprocessed_text


def document_text(document):
    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text

    return text
