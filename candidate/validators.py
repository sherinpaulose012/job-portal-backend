# candidate/validators.py

from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = [
    '.pdf',
    '.doc',
    '.docx'
]

def validate_resume(file):

    allowed = ['.pdf', '.doc', '.docx']

    if not file.name.lower().endswith(tuple(allowed)):
        raise ValidationError(
            "Invalid file type."
        )

    if file.size > 5 * 1024 * 1024:
        raise ValidationError(
            "File size must be below 5 MB."
        )    