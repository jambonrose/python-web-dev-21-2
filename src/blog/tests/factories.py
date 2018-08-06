"""Factory classes for blog models"""
from random import randint

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
)

from organizer.tests.factories import (
    StartupFactory,
    TagFactory,
)

from ..models import Post


class PostFactory(DjangoModelFactory):
    """Factory for Blog Post data"""

    title = Faker(
        "sentence", nb_words=3, variable_nb_words=True
    )
    slug = Faker("slug")
    text = Faker(
        "paragraph",
        nb_sentences=3,
        variable_nb_sentences=True,
    )
    pub_date = Faker("date_this_decade", before_today=True)

    class Meta:
        model = Post

    @post_generation
    def tags(  # noqa: N805
        post, create, extracted, **kwargs  # noqa: B902
    ):
        """Add related tag objects to Post"""
        if create:
            if extracted is not None:
                tag_list = extracted
            else:  # generate Tag objects randomly
                tag_list = map(
                    lambda f: f(),
                    [TagFactory] * randint(0, 5),
                )
            for tag in tag_list:
                post.tags.add(tag)

    @post_generation
    def startups(  # noqa: N805
        post, create, extracted, **kwargs  # noqa: B902
    ):
        """Add related startup objects to Post"""
        if create:
            if extracted is not None:
                startup_list = extracted
            else:  # generate Startup objects randomly
                startup_list = map(
                    lambda f: f(),
                    [StartupFactory] * randint(0, 2),
                )
            for startup in startup_list:
                post.startups.add(startup)
