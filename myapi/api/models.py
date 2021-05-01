from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (FileExtensionValidator,
                                    validate_image_file_extension)
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import PIL
from .validators import image_format_validator
from .thumbnails import create_thumbnail
from django.conf import settings


class User(AbstractUser):
    BASE = 'B'
    PREMIUM = 'P'
    ENTERPRISE = 'E'
    TYPE_CHOICES = [
        (BASE, 'Base'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    ]
    user_type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=BASE,
    )

    def save(self, *args, **kwargs):
        self.user_type.upper()
        super().save(*args, **kwargs)

    def is_premium(self):
        return self.user_type == 'P'

    def is_enterprise(self):
        return self.user_type == 'E'


class Image(models.Model):
    name = models.CharField(max_length=100, default='Photo')
    image = models.ImageField(
        upload_to='pics',
        blank=False,
        validators=[FileExtensionValidator(settings.ALLOWED_EXTENSIONS),
                    validate_image_file_extension,
                    ]
        )
    user = models.ForeignKey(User,
                             related_name='images',
                             on_delete=models.CASCADE)
    thumbnail_200 = models.FilePathField(
        path=f'{settings.MEDIA_ROOT}/pics',
        blank=True,
        null=True
    )
    thumbnail_400 = models.FilePathField(
        path=f'{settings.MEDIA_ROOT}/pics',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Image called '{self.name}' uploaded by {self.user.username}"

    def open_image(self):
        img = PIL.Image.open(self.image.path)
        return img

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = self.open_image()
        image_format_validator(img)

        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)

        img.save(self.image.path)

        if self.thumbnail_200 is None or self.thumbnail_400 is None:
            self.thumbnail_200 = create_thumbnail(self, 200)
            if self.user.is_premium() or self.user.is_enterprise():
                self.thumbnail_400 = create_thumbnail(self, 200)
            self.save()
        return





