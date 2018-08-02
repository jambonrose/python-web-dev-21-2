"""Factory classes for blog models"""
from factory import DjangoModelFactory

from ..models import Post


class PostFactory(DjangoModelFactory):
    """Factory for Blog Post data"""

    class Meta:
        model = Post
