"""Forms for the Organizer app"""
from django.core.exceptions import ValidationError
from django.forms import CharField, Form, SlugField

from .models import Tag


class TagForm(Form):
    """HTML form for Tag objects"""

    name = CharField(max_length=31)
    slug = SlugField(
        help_text="A label for URL config",
        max_length=31,
        required=False,
    )

    def clean_name(self):
        """Ensure Tag name is always lowercase"""
        return self.cleaned_data["name"].lower()

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

    def save(self):
        """Save the data in the bound form"""
        return Tag.objects.create(
            name=self.cleaned_data["name"],
            slug=self.cleaned_data["slug"],
        )
