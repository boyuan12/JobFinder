from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    min_salary = models.FloatField()
    max_salary = models.FloatField()
    freq = models.CharField(max_length=10)
    location = models.CharField(max_length=255)


class Qualification(models.Model):
    job_id = models.IntegerField()
    name = models.CharField(max_length=30)
