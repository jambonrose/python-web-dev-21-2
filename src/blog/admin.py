"""Configuration of Blog Admin panel"""
from django.contrib import admin

from .models import Post

admin.site.register(Post)
