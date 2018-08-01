"""Configuration of Organizer Admin panel"""
from django.contrib import admin

from .models import NewsLink, Startup, Tag

admin.site.register(NewsLink)
admin.site.register(Startup)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Configure Tag panel"""

    list_display = ("name", "slug")
