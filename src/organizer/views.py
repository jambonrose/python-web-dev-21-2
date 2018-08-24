"""Views for Organizer App"""
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import TagForm
from .models import Startup, Tag


class TagList(ListView):
    """Display a list of Tags"""

    queryset = Tag.objects.all()
    template_name = "tag/list.html"


class TagDetail(DetailView):
    """Display a single Tag"""

    queryset = Tag.objects.all()
    template_name = "tag/detail.html"


class TagCreate(View):
    """Create new Tags via HTML form"""

    def get(self, request):
        """Display an HTML form"""
        context = {"form": TagForm(), "update": False}
        return render(request, "tag/form.html", context)

    def post(self, request):
        """Handle Form submission: save Tag"""
        tform = TagForm(request.POST)
        if tform.is_valid():
            tag = tform.save()
            return redirect(tag.get_absolute_url())
        # invalid data; show form with errors
        context = {"form": tform, "update": False}
        return render(request, "tag/form.html", context)


class TagUpdate(View):
    """Update a Tag via HTML form"""

    def get(self, request, slug):
        """Display an HTML form with pre-filled data"""
        tag = get_object_or_404(Tag, slug=slug)
        context = {
            "tag": tag,
            "form": TagForm(instance=tag),
            "update": True,
        }
        return render(request, "tag/form.html", context)

    def post(self, request, slug):
        """Handle Form submission: save Tag"""
        tag = get_object_or_404(Tag, slug=slug)
        tform = TagForm(request.POST, instance=tag)
        if tform.is_valid():
            tag = tform.save()
            return redirect(tag.get_absolute_url())
        # invalid data; show form with errors
        context = {
            "tag": tag,
            "form": tform,
            "update": True,
        }
        return render(request, "tag/form.html", context)


class TagDelete(View):
    """Confirm and delete a Tag via HTML Form"""

    def get(self, request, slug):
        """Display an HTML form to confirm removal"""
        tag = get_object_or_404(Tag, slug=slug)
        return render(
            request, "tag/confirm_delete.html", {"tag": tag}
        )

    def post(self, request, slug):
        """Delete Tag"""
        tag = get_object_or_404(Tag, slug=slug)
        tag.delete()
        return redirect(reverse("tag_list"))


class StartupList(ListView):
    """Display a list of Startups"""

    queryset = Startup.objects.all()
    template_name = "startup/list.html"


class StartupDetail(DetailView):
    """Display a single Startup"""

    queryset = Startup.objects.all()
    template_name = "startup/detail.html"
