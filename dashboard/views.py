from django.contrib.auth import login
from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

# S3_ACCESS_KEY_ID
# S3_SECRET_ACCESS_KEY_ID

# Create your views here.
@login_required(login_url="/auth/login/")
def index(request):
    if request.session.get("role") is None:
        try:
            Profile.objects.get(user_id=request.user.id)
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