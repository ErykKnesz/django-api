from django.core.exceptions import ValidationError
from django.conf import settings


def image_format_validator(img):
    if img.format.upper() not in settings.ALLOWED_EXTENSIONS:
        raise ValidationError(
            "Only JPG/JPEG and PNG image extensions are allowed,"
            f" but {img.format.upper()} was provided."
        )