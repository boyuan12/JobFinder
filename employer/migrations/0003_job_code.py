# Generated by Django 3.1.4 on 2020-12-23 03:30

from django.db import migrations, models
import helpers


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0002_job_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='code',
            field=models.CharField(default=helpers.random_str, max_length=20),
        ),
    ]
