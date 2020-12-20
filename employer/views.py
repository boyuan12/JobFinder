from django.shortcuts import render
from dashboard.models import Profile

# Create your views here.
def index(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, "employer/index.html", {
        "name": profile.name
    })


def post_job(request):
    if request.method == "POST":
        pass

    else:
        return render(request, "employer/new.html")