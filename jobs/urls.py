from django.urls import path
from . import views

urlpatterns = [
    path("<str:code>/", views.view_job),
    path("apply/<str:code>/", views.apply_job),
    path("resume/<str:code>/", views.view_resume),
]