# Generated by Django 3.0.6 on 2020-05-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200516_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogposts',
            name='author_id',
            field=models.IntegerField(null=True),
        ),
    ]
