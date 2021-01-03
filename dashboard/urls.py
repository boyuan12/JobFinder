from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("complete-register/", views.complete_register),
    path("chat/<int:app_id>/", views.chat),
]