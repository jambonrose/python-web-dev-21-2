"""Factory classes for organizer models"""
from factory import DjangoModelFactory, Faker

from ..models import NewsLink, Startup, Tag


class TagFactory(DjangoModelFactory):
    """Factory for Tags (labels)"""

    name = Faker("domain_word")
    slug = Faker("slug")

    class Meta:
        model = Tag


class StartupFactory(DjangoModelFactory):
    """Factory for startup company data"""

    name = Faker("company")
    slug = Faker("slug")
    description = Faker("catch_phrase")
    founded_date = Faker(
        "date_this_decade", before_today=True
    )
    contact = Faker("company_email")
    website = Faker("url")

    class Meta:
        model = Startup


class NewsLinkFactory(DjangoModelFactory):
    """Factory for article links"""

    title = Faker(
        "sentence", nb_words=3, variable_nb_words=True
    )
    slug = Faker("slug")
    pub_date = Faker("date_this_decade", before_today=True)
    link = Faker("uri")

    class Meta:
        model = NewsLink
