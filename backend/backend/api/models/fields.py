from django.db import models
from io import BytesIO

from notebooks import PreprocessedText, StyleProfile


# TODO: Refactor classes from the notebooks library so that they implement a saveable
#       interface, and use that interface here.
class NBField(models.BinaryField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        # The bytes to save the object with are appended with either 0 or 1, based on
        # whether we are saving a PreprocessedText object or a StyleProfile object.
        if value[0] == b'\x00':
            bytes_io = BytesIO(value[1:])
            return PreprocessedText(bytes_io)

        if value[0] == b'\x01':
            bytes_io = BytesIO(value[1:])
            return StyleProfile(bytes_io)

    def to_python(self, value):
        if isinstance(value, PreprocessedText) or isinstance(value, StyleProfile) or value is None:
            return value

        if value[0] == 0:
            bytes_io = BytesIO(value[1:])
            return PreprocessedText(bytes_io)

        if value[0] == 1:
            bytes_io = BytesIO(value[1:])
            return StyleProfile(bytes_io)

    def get_prep_value(self, value):
        binary = value.binary.getvalue()

        if isinstance(value, PreprocessedText):
            return b"\x00" + binary

        if isinstance(value, StyleProfile):
            return b"\x01" + binary
