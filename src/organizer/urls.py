"""URL Configuration for Organizer App"""
from django.urls import path

from .views import HelloWorld

urlpatterns = [
    path("", HelloWorld.as_view(), name="hello_world")
]
