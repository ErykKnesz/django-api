# Generated by Django 3.2 on 2021-05-09 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20210509_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='thumbnail_400',
            new_name='big_thumbnail',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='thumbnail_200',
            new_name='small_thumbnail',
        ),
    ]
