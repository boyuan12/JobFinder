from django.http.response import JsonResponse
from helpers import get_s3
from django.shortcuts import render
from dashboard.models import Profile, ChatMessage
from .models import Job, Qualification
from django.http import HttpResponseRedirect
from jobs.models import Application
from django.contrib.auth.models import User
import requests
import json
from django.http import HttpResponse


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
        profile1 = Profile.objects.get(user_id=app.applicant_id)
        profile2 = Profile.objects.get(user_id=request.user.id)
        return render(request, "employer/chat.html", {
            "messages": messages,
            "app": app,
            "job": job,
            "profile1": profile1, # candidate
            "profile2": profile2 # employer
        })


def schedule_interview(request):
    if request.method == "POST":

        candidate = User.objects.get(id=int(request.POST["candidate"]))
        candidate_profile = Profile.objects.get(user_id=candidate.id)
        app = Application.objects.get(applicant_id=candidate.id, job_id=int(request.POST["job"]))

        data = requests.post("https://api.zoom.us/v2/users/me/meetings", headers={
            'content-type': "application/json",
            "authorization": f"Bearer {request.session['zoom_access_token']}"
        }, data=json.dumps({
            "topic": f"Interview with {candidate_profile.name}",
            "type": 2,
            "start_time": request.POST["time"],
        }))

        print(data.json()["join_url"], data.json()["start_url"])

        ChatMessage(from_id=request.user.id, to_id=candidate.id, application_id=app.id, message=f"Hello! Your interview been successfully created! Please join this <a href='{data.json()['join_url']}'>Zoom meeting</a> on {data.json()['start_time']} UTC. Good Luck!").save()

        ChatMessage(from_id=request.user.id, to_id=candidate.id, application_id=app.id, message=f"This is only viewable to you, to start the Zoom meeting, click this <a href='{data.json()['start_url']}'>link</a>.", public=False).save()


        return HttpResponseRedirect(f"/employer/chat/{app.id}")

    else:
        profile = Profile.objects.get(user_id=request.user.id)
        jobs = Job.objects.filter(profile=profile.id)
        return render(request, "employer/schedule-interview.html", {
            "jobs": jobs,
        })


def job_candidates(request, job_id):
    apps = Application.objects.filter(job_id=job_id)
    candidates = []
    for a in apps:
        user = User.objects.get(id=a.applicant_id)
        profile = Profile.objects.get(user_id=user.id)
        candidates.append([user.id, profile.name])
    return JsonResponse(candidates, safe=False)


def reject_candidate(request, app_id):
    app = Application.objects.get(id=app_id)
    app.status = 2
    app.save()
    return HttpResponse("Rejected")


def reject_candidate(request, app_id):
    app = Application.objects.get(id=app_id)
    app.status = 3
    app.save()
    return HttpResponse("Hired")

