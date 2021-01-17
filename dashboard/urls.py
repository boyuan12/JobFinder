from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("complete-register/", views.complete_register),
    path("chat/<int:app_id>/", views.chat),
    path("zoom/callback/", views.zoom_callback),
    path("dashboard/", views.search_job),
    path("apps/", views.view_apps)
]