import os

from prompt_toolkit.validation import Validator, ValidationError


class PathValidation(Validator):
    def validate(self, document):
        if not os.path.exists(document.text):
            raise ValidationError(
                message='Please enter a valid path',
                cursor_position=len(document.text)
            )