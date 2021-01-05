from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("new/", views.post_job),
    path("jobs/", views.view_all_jobs),
    path("apps/", views.view_all_application),
    path("app/<int:id>/", views.view_application),
    path("chat/<int:app_id>/", views.chat_with_candidate),
    path("schedule-interview/", views.schedule_interview),
    path("job/candidate/<int:job_id>/", views.job_candidates)
]