# Generated by Django 4.2.2 on 2023-06-25 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_project_locations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='project',
        ),
        migrations.RemoveField(
            model_name='project',
            name='locations',
        ),
        migrations.AddField(
            model_name='location',
            name='projects',
            field=models.ManyToManyField(to='main_app.project'),
        ),
        migrations.DeleteModel(
            name='Deck',
        ),
    ]
