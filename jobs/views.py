from django.shortcuts import render
from employer.models import Job, Qualification
from dashboard.models import Profile

# Create your views here.
def view_job(request, code):
    
    job = Job.objects.get(code=code)
    qualificatons = Qualification.objects.filter(job_id=job.id)
    company = Profile.objects.get(id=job.profile).name

    return render(request, "jobs/job.html", {
        "job": job,
        "qs": qualificatons,
        "company": company
    })

