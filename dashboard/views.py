from employer.models import Job
from jobs.models import Application
from django.contrib.auth import login
from django.shortcuts import render
from .models import ChatMessage, Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

# S3_ACCESS_KEY_ID
# S3_SECRET_ACCESS_KEY_ID

# Create your views here.
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
    return HttpResponse("Welcome to the dashboard!")


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
        return HttpResponseRedirect("/chat/2/")
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