from dashboard.models import Profile
from django.db import models
import helpers

# Create your models here.
class Job(models.Model):
    profile = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    min_salary = models.FloatField()
    max_salary = models.FloatField()
    freq = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    code = models.CharField(max_length=20, default=helpers.random_str)
    timestamp = models.DateTimeField(auto_now=True)


class Qualification(models.Model):
    job_id = models.IntegerField()
    name = models.CharField(max_length=30)
