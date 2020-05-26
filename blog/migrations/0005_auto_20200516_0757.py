# Generated by Django 3.0.6 on 2020-05-16 07:57

from django.db import migrations, models

def fillauthor(apps,schema_editor):
    authmodel = apps.get_model("auth","user")
    print(authmodel.objects.all())

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200516_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogposts',
            name='post_content',
            field=models.TextField(),
        ),
        migrations.RunPython(fillauthor),
    ]
