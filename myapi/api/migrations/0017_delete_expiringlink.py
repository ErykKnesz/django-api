# Generated by Django 3.2 on 2021-09-21 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20210509_1504'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExpiringLink',
        ),
    ]