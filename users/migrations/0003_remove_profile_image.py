# Generated by Django 3.0.6 on 2020-06-05 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]
