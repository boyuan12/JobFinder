from django.shortcuts import render
from employer.models import Job, Qualification
from dashboard.models import Profile
from .models import Application

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


def apply_job(request, code):
    if request.method == "POST":
        applicant_id = request.user.id
        job_id = Job.objects.get(code=code).id


    else:
        job = Job.objects.get(code=code)
        company = Profile.objects.get(id=job.profile).name
        profile = Profile.objects.get(user_id=request.user.id)
        return render(request, "jobs/apply.html", {
            "job": job,
            "company": company,
            "profile": profile
        })

