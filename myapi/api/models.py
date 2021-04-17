from django.db import models
from django.contrib.auth.models import AbstractUser
import PIL
from django.core.validators import (FileExtensionValidator,
                                    validate_image_file_extension)


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

    def get_images(self):
        pass


class Image(models.Model):
    name = models.CharField(max_length=100, default='Photo')
    image = models.ImageField(
        upload_to='pics',
        blank=False,
        validators=[FileExtensionValidator(['JPEG', 'PNG']),
                    validate_image_file_extension,
                    ]
        )
    owner = models.ForeignKey(User,
                              related_name='images',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f"Image called '{self.name}' uploaded by {self.owner.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = PIL.Image.open(self.image.path)
        file_extension = img.format
        if file_extension.upper() == 'JPEG' or file_extension.upper() == 'PNG':
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)







