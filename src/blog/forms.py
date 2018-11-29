"""Forms for the Blog app"""
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    """HTML form for Post objects"""

    class Meta:
        model = Post
        fields = "__all__"
