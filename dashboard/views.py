from employer.models import Job
from jobs.models import Application
from django.contrib.auth import login
from django.shortcuts import render
from .models import ChatMessage, Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import requests
import math

# S3_ACCESS_KEY_ID
# S3_SECRET_ACCESS_KEY_ID

# Create your views here.
def base64_encode(message):
    import base64
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


@login_required(login_url="/auth/login/")
def index(request):

    if request.session.get("role") is None:
        try:
            p = Profile.objects.get(user_id=request.user.id)
            request.session["role"] = int(p.role)
            if int(p.role) == 0:
                return HttpResponseRedirect("/employer/")
        except Profile.DoesNotExist:
            return HttpResponseRedirect("/complete-register/")

    elif int(request.session.get("role")) == 0:
        return HttpResponseRedirect("/employer/")
    return HttpResponseRedirect("/dashboard/")


@login_required(login_url="/auth/login/")
def complete_register(request):
    if request.method == "POST":
        role = int(request.POST.get("role"))
        name = request.POST.get("name")

        Profile(user_id=request.user.id, role=role, name=name).save()

        request.session["role"] = int(request.POST.get("role"))

        return HttpResponseRedirect("/")
    else:
        return render(request, "dashboard/complete-register.html")


@login_required(login_url="/auth/login/")
def chat(request, app_id):
    if request.method == "POST":
        message = request.POST["message"]
        to_id = Application.objects.get(id=app_id).applicant_id
        ChatMessage(from_id=request.user.id, to_id=to_id, application_id=app_id, message=message).save()
        return HttpResponseRedirect(f"/chat/{app_id}/")
    else:
        app = Application.objects.get(id=app_id)
        messages = ChatMessage.objects.filter(application_id=app_id)
        job = Job.objects.get(id=app.job_id)
        profile1 = Profile.objects.get(user_id=app.applicant_id)
        profile2 = Profile.objects.get(id=job.profile)
        return render(request, "dashboard/chat.html", {
            "messages": messages,
            "app": app,
            "job": job,
            "profile1": profile1, # candidate
            "profile2": profile2 # employer
        })


def zoom_callback(request):
    code = request.GET["code"]
    data = requests.post(f"https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=http://127.0.0.1:8000/zoom/callback/", headers={
        "Authorization": "Basic " + base64_encode("k8SPArNSai_zq5rbE0SmA:l8JCpZsZ815TxBz79SgtaHds1sGYgV86")
    })
    print(data.text)
    request.session["zoom_access_token"] = data.json()["access_token"]

    return HttpResponseRedirect("/employer/schedule-interview/")


def search_job(request):
    if request.GET.get("q"):
        # search for the job
        jobs = Job.objects.filter(title__contains=request.GET.get("q"))
        total_jobs = len(jobs)
        if request.GET.get("p"):
            p = int(request.GET.get("p"))
            if p == 1:
                jobs = Job.objects.filter(title__contains=request.GET.get("q"))[0:5] 
            else:
                jobs = Job.objects.filter(title__contains=request.GET.get("q"))[5*p-5:5*p] # 2: 5 - 9

        return render(request, "dashboard/searched.html", {
            "jobs": jobs,
            "pagination": [i+1 for i in range(math.ceil(total_jobs/5))],
            "current_page": "".join(['None' if request.GET.get("p") == None else request.GET.get("p")]),
            "q": request.GET.get("q"),
        })
    else:
        return render(request, "dashboard/index.html")


@login_required(login_url="/auth/login/")
def view_apps(request):
    data = []
    apps = Application.objects.filter(applicant_id=request.user.id)
    for a in apps:
        job = Job.objects.get(id=a.job_id)
        data.append([job, a])
    return render(request, "dashboard/apps.html", {
        "apps": data
    })

