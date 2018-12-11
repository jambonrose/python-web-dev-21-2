"""Forms for the Organizer app"""
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import HiddenInput

from .models import NewsLink, Startup, Tag


class LowercaseNameMixin:
    """Form cleaner to lower case of name field"""

    def clean_name(self):
        """Ensure Tag name is always lowercase"""
        return self.cleaned_data["name"].lower()


class SlugCleanMixin:
    """Mixin class to ensure slug field is not create"""

    def clean_slug(self):
        """Ensure slug is not 'create'

        This is an oversimplification!!! See the following
        link for how to raise the error correctly.

        https://docs.djangoproject.com/en/2.1/ref/forms/validation/#raising-validationerror

        """
        slug = self.cleaned_data["slug"]
        if slug == "create":
            raise ValidationError(
                "Slug may not be 'create'."
            )
        return slug


class TagForm(LowercaseNameMixin, ModelForm):
    """HTML form for Tag objects"""

    class Meta:
        model = Tag
        fields = "__all__"  # name only, no slug!


class StartupForm(
    LowercaseNameMixin, SlugCleanMixin, ModelForm
):
    """HTML form for Startup objects"""

    class Meta:
        model = Startup
        fields = "__all__"


class NewsLinkForm(ModelForm):
    """HTML form for NewsLink objects"""

    class Meta:
        model = NewsLink
        fields = "__all__"
        widgets = {"startup": HiddenInput()}

    def clean_slug(self):
        """Avoid URI conflicts with paths in app"""
        slug = self.cleaned_data["slug"]
        if slug in ["delete", "update", "add_article"]:
            raise ValidationError(
                f"Slug may not be '{slug}'."
            )
        return slug
