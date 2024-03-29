# Generated by Django 3.2 on 2021-04-24 21:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='thumbnail_200',
            field=models.ImageField(blank=True, null=True, upload_to='pics/thumbnails'),
        ),
        migrations.AddField(
            model_name='image',
            name='thumbnail_400',
            field=models.ImageField(blank=True, null=True, upload_to='pics/thumbnails'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='pics', validators=[django.core.validators.FileExtensionValidator(['JPG', 'JPEG', 'PNG']), django.core.validators.validate_image_file_extension]),
        ),
    ]
