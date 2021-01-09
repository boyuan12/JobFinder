from django.db import models

# Create your models here.
class Profile(models.Model):
    user_id = models.IntegerField()
    role = models.IntegerField() # 0: employer/HR, 1: job seeker
    name = models.CharField(max_length=255)


class ChatMessage(models.Model):
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    application_id = models.IntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)
