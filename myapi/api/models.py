from django.db import models
from django.contrib.auth.models import AbstractUser
import PIL


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



class Image(models.Model):
    name = models.CharField(max_length=100, default='Photo')
    image = models.ImageField(upload_to='pics', blank=False)
    owner = models.ForeignKey(User,
                              related_name='images',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f"Image called '{self.name}' uploaded by {self.owner.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = PIL.Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)







