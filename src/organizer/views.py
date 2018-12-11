"""Views for Organizer App"""
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)

from .forms import NewsLinkForm, StartupForm, TagForm
from .models import NewsLink, Startup, Tag


class NewsLinkObjectMixin:
    """Django View mix-in to find NewsLinks"""

    model = NewsLink

    def get_object(self, queryset=None):
        """Get NewsLink from database

        http://ccbv.co.uk/SingleObjectMixin
        """
        if queryset is None:
            if hasattr(self, "get_queryset"):
                queryset = self.get_queryset()
            else:
                queryset = self.model.objects.all()

        # Django's View class puts URI kwargs in dictionary
        startup_slug = self.kwargs.get("startup_slug")
        newslink_slug = self.kwargs.get("newslink_slug")

        if startup_slug is None or newslink_slug is None:
            raise AttributeError(
                f"View {self.__class__.__name__} must be"
                f"called with a slug for a Startup and a"
                f"slug for a NewsLink objects."
            )

        return get_object_or_404(
            queryset,
            startup__slug=startup_slug,
            slug=newslink_slug,
        )


class NewsLinkContextMixin:
    """Add Startup to template context in NewsLink views"""

    def get_context_data(self, **kwargs):
        """Dynamically add to template context

        http://ccbv.co.uk/ContextMixin
        """
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        return super().get_context_data(
            startup=startup, **kwargs
        )


class VerifyStartupFkToUriMixin:
    """Mixin to verify Startup data in NewsLink views

    NewsLink creation and updating views specify the Startup slug in the URI.
    However, for simplicity when interacting with the NewsLinkForm, the form
    also has a field for the Startup object. This class ensures that the
    Startup referred to by the URI and by the NewsLinkForm field is one and
    the same
    """

    def verify_startup_fk_matches_uri(self):
        """Raise HTTP 400 if Startup data mismatched"""
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        form_startup_pk = self.request.POST.get("startup")
        if str(startup.pk) != form_startup_pk:
            raise SuspiciousOperation(
                "Startup Form PK and URI do not match"
            )

    def post(self, request, *args, **kwargs):
        """Check Startup data before form submission process

        - Raise HTTP 400 if Startup data mismatched
        - Hook into Generic Views for rest of work
        """
        self.verify_startup_fk_matches_uri()
        return super().post(request, *args, **kwargs)


class NewsLinkCreate(
    VerifyStartupFkToUriMixin,
    NewsLinkContextMixin,
    CreateView,
):
    """Create a link to an article about a startup"""

    extra_context = {"update": False}
    form_class = NewsLinkForm
    model = NewsLink
    template_name = "newslink/form.html"

    def get_initial(self):
        """Pre-select Startup in NewsLinkForm"""
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        return dict(
            super().get_initial(), startup=startup.pk
        )


class NewsLinkDelete(
    NewsLinkObjectMixin, NewsLinkContextMixin, DeleteView
):
    """Delete a link to an article about a startup"""

    template_name = "newslink/confirm_delete.html"

    def get_success_url(self):
        """Return the detail page of the Startup parent

        http://ccbv.co.uk/DeletionMixin
        """
        startup = get_object_or_404(
            Startup, slug=self.kwargs.get("startup_slug")
        )
        return startup.get_absolute_url()


class NewsLinkDetail(NewsLinkObjectMixin, RedirectView):
    """Redirect to Startup Detail page

    http://ccbv.co.uk/RedirectView/
    """

    def get_redirect_url(self, *args, **kwargs):
        """Redirect user to Startup page"""
        return self.get_object().get_absolute_url()


class NewsLinkUpdate(
    VerifyStartupFkToUriMixin,
    NewsLinkObjectMixin,
    NewsLinkContextMixin,
    UpdateView,
):
    """Update a link to an article about a startup"""

    extra_context = {"update": True}
    form_class = NewsLinkForm
    template_name = "newslink/form.html"


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


class StartupDelete(DeleteView):
    """Confirm and delete a Startup via HTML Form"""

    model = Startup
    template_name = "startup/confirm_delete.html"
    success_url = reverse_lazy("startup_list")


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
