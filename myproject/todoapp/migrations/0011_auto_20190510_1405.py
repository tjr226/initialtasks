# Generated by Django 2.2 on 2019-05-10 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0010_taskmodel_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskmodel',
            old_name='project',
            new_name='why',
        ),
    ]
