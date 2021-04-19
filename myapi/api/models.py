from django.db import models
from django.contrib.auth.models import AbstractUser
import PIL
from django.core.validators import (FileExtensionValidator,
                                    validate_image_file_extension)
from .validators import image_format_validator


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
        #default=BASE,
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
        validators=[FileExtensionValidator(['JPG', 'JPEG',  'PNG']),
                    validate_image_file_extension,
                    ]
        )
    owner = models.ForeignKey(User,
                              related_name='images',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f"Image called '{self.name}' uploaded by {self.owner.username}"

    def open_image(self):
        img = PIL.Image.open(self.image.path)
        return img

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = self.open_image()
        image_format_validator(img)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def set_thumbnails(self, queryset, user):
        img = queryset.open_image()
        small_size = (200, img.width)
        small_thumbnail = img.thumbnail(small_size)
        big_size = (400, img.width)
        big_thumbnail = img.thumbnail(big_size)
        if user.is_premium():
            return small_thumbnail, big_thumbnail
        elif user.is_enterprise():
            pass
        return small_thumbnail



