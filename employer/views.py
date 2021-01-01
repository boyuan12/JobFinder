from helpers import get_s3
from django.shortcuts import render
from dashboard.models import Profile, ChatMessage
from .models import Job, Qualification
from django.http import HttpResponseRedirect
from jobs.models import Application
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, "employer/index.html", {
        "name": profile.name
    })


def post_job(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        qualification = request.POST["qualification"]
        min_salary = request.POST["min"]
        max_salary = request.POST["max"]
        pay_frequency = request.POST["rate"]
        location = request.POST["location"]

        profile = Profile.objects.get(user_id=request.user.id)

        Job.objects.create(profile=profile.id, title=title, description=description, min_salary=min_salary, max_salary=max_salary, freq=pay_frequency, location=location).save()

        job = Job.objects.all()[::-1][0]

        qs = qualification.split(",")
        for i in qs:
            Qualification(job_id=job.id, name=i).save()

        return HttpResponseRedirect(f"/jobs/{job.code}")

    else:
        return render(request, "employer/new.html")


def view_all_jobs(request):
    profile = Profile.objects.get(user_id=request.user.id)
    jobs = Job.objects.filter(profile=profile.id)

    return render(request, "employer/all.html", {
        "jobs": jobs
    })


def view_all_application(request):
    unread_apps = []
    profile = Profile.objects.get(user_id=request.user.id)
    jobs = Job.objects.filter(profile=profile.id)

    for job in jobs:
        apps = Application.objects.filter(status=0, job_id=job.id)
        for app in apps:
            name = Profile.objects.get(user_id=app.applicant_id).name
            email = User.objects.get(id=app.applicant_id)
            time = app.timestamp
            unread_apps.append([name, email, job.title, time, app.id])

    return render(request, "employer/applications.html", {
        "apps": unread_apps
    })


def view_application(request, id):
    app = Application.objects.get(id=id)
    app.status = 1
    job = Job.objects.get(id=app.job_id)
    user = User.objects.get(id=app.applicant_id)
    profile = Profile.objects.get(user_id=user.id)
    return render(request, "employer/application.html", {
        "app": app,
        "job": job,
        "user": user,
        "profile": profile
    })


def chat_with_candidate(request, app_id):
    if request.method == "POST":
        message = request.POST["message"]
        to_id = Application.objects.get(id=app_id).applicant_id
        ChatMessage(from_id=request.user.id, to_id=to_id, application_id=app_id, message=message).save()
        return HttpResponseRedirect("/employer/chat/2/")
    else:
        app = Application.objects.get(id=app_id)
        messages = ChatMessage.objects.filter(application_id=app_id)
        job = Job.objects.get(id=app.job_id)
        profile = Profile.objects.get(user_id=app.applicant_id)
        return render(request, "employer/chat.html", {
            "messages": messages,
            "app": app,
            "job": job,
            "profile": profile
        })