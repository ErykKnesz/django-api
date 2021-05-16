from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from django.core.validators import (FileExtensionValidator,
                                    validate_image_file_extension,
                                    MaxValueValidator, MinValueValidator)
import PIL
import os
from django.conf import settings


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
    small_thumbnail = models.ImageField(
        upload_to='pics',
        blank=True,
        null=True,
    )
    big_thumbnail = models.ImageField(
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
        small_thmb = self.__dict__['small_thumbnail']
        big_thmb = self.__dict__['big_thumbnail']
        if not small_thmb:
            self.create_thumbnail(self.small_thumbnail,
                                  self.user.account.small_thmb_size)
        if not big_thmb:
            if not self.user.account.is_base():
                self.create_thumbnail(self.big_thumbnail,
                                      self.user.account.big_thmb_size)

    def get_expiring_link(self, duration):
        pass


class Account(models.Model):
    BASE = 'B'
    PREMIUM = 'P'
    ENTERPRISE = 'E'
    CUSTOM = 'C'
    TYPE_CHOICES = [
        (BASE, 'Base'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
        (CUSTOM, 'Custom'),
    ]
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=BASE,
    )

    small_thmb_size = models.IntegerField(default=200)
    big_thmb_size = models.IntegerField(default=400)
    has_original_img = models.BooleanField(default=False)
    has_expiring_links = models.BooleanField(default=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def is_base(self):
        return self.type == 'B'

    def is_premium(self):
        return self.type == 'P'

    def is_enterprise(self):
        return self.type == 'E'

    def is_custom(self):
        return self.type == 'C'

    def save(self, *args, **kwargs):
        if not self.is_custom:
            self.small_thmb_size = 200
            if self.is_premium() or self.is_enterprise():
                self.big_thmb_size = 400
                self.has_original_img = True
            if self.is_enterprise():
                self.has_expiring_links = True
            self.type.upper()
        super().save(*args, **kwargs)


class ExpiringLink(models.Model):
    account = models.OneToOneField(Account,
                                   on_delete=models.CASCADE,
                                   primary_key=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    link_max_life = models.IntegerField(default=30,
                                        validators=[MaxValueValidator(30000),
                                                    MinValueValidator(30)])
    link_start = models.DateTimeField(auto_now_add=True)