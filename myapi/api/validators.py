from django.core.exceptions import ValidationError


def image_format_validator(img):
    if img.format.upper() not in ('JPG', 'JPEG', 'PNG'):
        raise ValidationError(
            "Only JPG/JPEG and PNG image extensions are allowed,"
            f" but {img.format.upper()} was provided."
        )