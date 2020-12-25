from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("new/", views.post_job),
    path("jobs/", views.view_all_jobs),
]