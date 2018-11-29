"""Views for Organizer App"""
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import StartupForm, TagForm
from .models import Startup, Tag


class TagList(ListView):
    """Display a list of Tags"""

    queryset = Tag.objects.all()
    template_name = "tag/list.html"


class TagDetail(DetailView):
    """Display a single Tag"""

    queryset = Tag.objects.all()
    template_name = "tag/detail.html"


class TagCreate(CreateView):
    """Create new Tags via HTML form"""

    form_class = TagForm
    model = Tag
    template_name = "tag/form.html"
    extra_context = {"update": False}


class TagUpdate(UpdateView):
    """Update a Tag via HTML form"""

    form_class = TagForm
    model = Tag
    template_name = "tag/form.html"
    extra_context = {"update": True}


class TagDelete(DeleteView):
    """Confirm and delete a Tag via HTML Form"""

    model = Tag
    template_name = "tag/confirm_delete.html"
    success_url = reverse_lazy("tag_list")


class StartupCreate(CreateView):
    """Create new Startups via HTML form"""

    form_class = StartupForm
    model = Startup
    template_name = "startup/form.html"
    extra_context = {"update": False}


class StartupList(ListView):
    """Display a list of Startups"""

    queryset = Startup.objects.all()
    template_name = "startup/list.html"


class StartupDetail(DetailView):
    """Display a single Startup"""

    queryset = Startup.objects.all()
    template_name = "startup/detail.html"


class StartupUpdate(UpdateView):
    """Update a Startup via HTML form"""

    form_class = StartupForm
    model = Startup
    template_name = "startup/form.html"
    extra_context = {"update": True}
