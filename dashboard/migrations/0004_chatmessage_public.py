# Generated by Django 3.1.4 on 2021-01-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
