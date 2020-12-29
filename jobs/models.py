from django.db import models

# Create your models here.
class Application(models.Model):
    applicant_id = models.IntegerField()
    job_id = models.IntegerField()
    resume = models.CharField(max_length=10)
    cover_letter = models.TextField()
