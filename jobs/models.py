from django.db import models

# Create your models here.
class Application(models.Model):
    applicant_id = models.IntegerField()
    job_id = models.IntegerField()
    resume = models.CharField(max_length=10)
    cover_letter = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0) # 0: waiting response, 1: viewed, 2: rejected, 3: hired
