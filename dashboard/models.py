from django.db import models

# Create your models here.
class Profile(models.Model):
    user_id = models.IntegerField()
    role = models.IntegerField() # 0: employer/HR, 1: job seeker
    name = models.CharField(max_length=255)
