"""Factory classes for organizer models"""
from random import randint

from factory import (
    DjangoModelFactory,
    Faker,
    Sequence,
    SubFactory,
    post_generation,
)

from ..models import NewsLink, Startup, Tag


class TagFactory(DjangoModelFactory):
    """Factory for Tags (labels)"""

    name = Sequence(lambda n: f"name-{n}")
    slug = Sequence(lambda n: f"slug-{n}")

    class Meta:
        model = Tag


class StartupFactory(DjangoModelFactory):
    """Factory for startup company data"""

    name = Sequence(lambda n: f"name-{n}")
    slug = Sequence(lambda n: f"slug-{n}")
    description = Faker("catch_phrase")
    founded_date = Faker(
        "date_this_decade", before_today=True
    )
    contact = Faker("company_email")
    website = Faker("url")

    class Meta:
        model = Startup

    @post_generation
    def tags(  # noqa: N805
        startup, create, extracted, **kwargs  # noqa: B902
    ):
        """Add related tag objects to Startup"""
        if create:
            if extracted is not None:
                tag_list = extracted
            else:  # generate Tag objects randomly
                tag_list = map(
                    lambda f: f(),
                    [TagFactory] * randint(0, 5),
                )
            for tag in tag_list:
                startup.tags.add(tag)


class NewsLinkFactory(DjangoModelFactory):
    """Factory for article links"""

    title = Faker(
        "sentence", nb_words=3, variable_nb_words=True
    )
    slug = Sequence(lambda n: f"slug-{n}")
    pub_date = Faker("date_this_decade", before_today=True)
    link = Faker("uri")
    startup = SubFactory(StartupFactory)

    class Meta:
        model = NewsLink
