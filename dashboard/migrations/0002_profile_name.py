# Generated by Django 3.1.4 on 2020-12-19 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
