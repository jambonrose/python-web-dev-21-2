"""Root URL Configuration for Startup Organizer Project"""
from django.contrib import admin
from django.urls import include, path

from blog.urls import urlpatterns as blog_urls
from organizer.urls import urlpatterns as organizer_urls

api_urls = blog_urls + organizer_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_urls)),
]
