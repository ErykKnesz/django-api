# Generated by Django 3.2 on 2021-05-01 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20210428_2333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='owner',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='image',
            name='thumbnail_200',
        ),
        migrations.RemoveField(
            model_name='image',
            name='thumbnail_400',
        ),
    ]