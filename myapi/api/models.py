from django.db import models
from django.core.files import File
from django.contrib.auth.models import AbstractUser
from django.core.validators import (FileExtensionValidator,
                                    validate_image_file_extension)
import PIL
import os
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
    thumbnail_200 = models.ImageField(
        upload_to='pics',
        blank=True,
        null=True,
    )
    thumbnail_400 = models.ImageField(
        upload_to='pics',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Image called '{self.name}' uploaded by {self.user.username}"

    def _create_thumbnail_name(self, height):
        name = self.image.name
        name = os.path.basename(name)
        name_suffix = f'_thumbnail{height}'
        if name.lower().endswith('.jpg') or name.lower().endswith('.png'):
            ext = name[-4:]
            name = name[:-4]
        if name.lower().endswith('.jpeg'):
            ext = name[-5:]
            name = name[:-5]
        name = name + name_suffix + ext
        return name

    def create_thumbnail(self, image_thmb_field, height):
        with open(self.image.path, 'rb') as f:
            image_thmb_field.save(
                f'{self._create_thumbnail_name(height)}',
                File(f))
            img = PIL.Image.open(image_thmb_field.path)
            output_size = (height, img.width)
            img.thumbnail(output_size)
            img.save(image_thmb_field.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        thmb_200 = self.__dict__['thumbnail_200']
        thmb_400 = self.__dict__['thumbnail_400']
        if not thmb_200:
            self.create_thumbnail(self.thumbnail_200, 200)
        if not thmb_400:
            if self.user.is_premium() or self.user.is_enterprise():
                self.create_thumbnail(self.thumbnail_400, 400)
