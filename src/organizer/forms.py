"""Forms for the Organizer app"""
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Tag


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


class TagForm(ModelForm):
    """HTML form for Tag objects"""

    class Meta:
        model = Tag
        fields = "__all__"  # name only, no slug!

    def clean_name(self):
        """Ensure Tag name is always lowercase"""
        return self.cleaned_data["name"].lower()
