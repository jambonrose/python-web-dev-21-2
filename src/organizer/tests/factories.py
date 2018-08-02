"""Factory classes for organizer models"""
from factory import DjangoModelFactory

from ..models import NewsLink, Startup, Tag


class TagFactory(DjangoModelFactory):
    """Factory for Tags (labels)"""

    class Meta:
        model = Tag


class StartupFactory(DjangoModelFactory):
    """Factory for startup company data"""

    class Meta:
        model = Startup


class NewsLinkFactory(DjangoModelFactory):
    """Factory for article links"""

    class Meta:
        model = NewsLink
