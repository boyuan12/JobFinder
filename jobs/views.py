from django.http import HttpResponse
from django.shortcuts import render
from employer.models import Job, Qualification
from dashboard.models import Profile
from .models import Application
from helpers import upload_s3, get_s3

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
    try:
        app = Application.objects.get(applicant_id=request.user.id, job_id=Job.objects.get(code=code).id)
        return render(request, "authentication/success.html", {
            "message": f"You already applied to this job on {app.timestamp} UTC"
        })
    except Application.DoesNotExist:
        pass

    if request.method == "POST":
        applicant_id = request.user.id
        job_id = Job.objects.get(code=code).id

        file_code = upload_s3(request)

        Application(applicant_id=applicant_id, job_id=job_id, resume=file_code, cover_letter=request.POST["cover"]).save()

        return render(request, "authentication/success.html", {
            "message": "Applied successfully!"
        })

    else:
        job = Job.objects.get(code=code)
        company = Profile.objects.get(id=job.profile).name
        profile = Profile.objects.get(user_id=request.user.id)
        return render(request, "jobs/apply.html", {
            "job": job,
            "company": company,
            "profile": profile
        })


def view_resume(request, code):
    file_data = get_s3(code)
    response = HttpResponse(file_data["Body"])
    response["Content-Type"] = "application/pdf"
    return response

