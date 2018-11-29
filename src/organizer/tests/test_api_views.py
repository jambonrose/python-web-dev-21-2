"""Tests for Organizer Views"""
import json
from functools import partial

from test_plus import APITestCase

from config.test_utils import (
    context_kwarg,
    get_instance_data,
    lmap,
    omit_keys,
    reverse,
)

from ..models import NewsLink, Startup, Tag
from ..serializers import (
    NewsLinkSerializer,
    StartupSerializer,
    TagSerializer,
)
from .factories import (
    NewsLinkFactory,
    StartupFactory,
    TagFactory,
)


def get_tag_data(tag):
    """Strip unchecked fields from Tag"""
    return omit_keys("id", get_instance_data(tag))


omit_url = partial(omit_keys, "url")


class TagAPITests(APITestCase):
    """Test API Views for Tag objects"""

    maxDiff = None

    @property
    def response_json(self):
        """Shortcut to obtain JSON from last response"""
        return json.loads(self.last_response.content)

    def test_list(self):
        """Is there a list of Tag objects"""
        url_name = "api-tag-list"
        tag_list = TagFactory.create_batch(10)
        self.get_check_200(url_name)
        self.assertCountEqual(
            self.response_json,
            TagSerializer(
                tag_list,
                many=True,
                **context_kwarg(reverse(url_name))
            ).data,
        )

    def test_list_empty(self):
        """Do we return an empty list if no tags?"""
        self.get_check_200("api-tag-list")
        self.assertEquals(self.response_json, [])

    def test_list_create(self):
        """Does Tag list view create new objects via POST?"""
        self.assertEqual(Tag.objects.count(), 0)
        self.post("api-tag-list", data={"name": "django"})
        self.response_201()
        self.assertEqual(Tag.objects.count(), 1)

    def test_detail(self):
        """Is there a detail view for a Tag object"""
        tag = TagFactory()
        url = reverse("api-tag-detail", slug=tag.slug)
        self.get_check_200(url)
        self.assertCountEqual(
            self.response_json,
            TagSerializer(tag, **context_kwarg(url)).data,
        )

    def test_detail_404(self):
        """Do we generate 404 if tag not found?"""
        self.get("api-tag-detail", slug="nonexistent")
        self.response_404()

    def test_detail_update(self):
        """Can we update a Tag via PUT?"""
        tag = TagFactory(name="first")
        url = reverse("api-tag-detail", slug=tag.slug)
        self.put(url, data={"name": "second"})
        self.response_200()
        tag.refresh_from_db()
        self.assertEqual(tag.name, "second")

    def test_detail_update_404(self):
        """Do we generate 404 if tag not found?"""
        url = reverse("api-tag-detail", slug="nonexistent")
        self.put(url, data={"name": "second"})
        self.response_404()

    def test_detail_partial_update(self):
        """Can we update a Tag via PATCH?"""
        tag = TagFactory(name="first")
        url = reverse("api-tag-detail", slug=tag.slug)
        self.patch(url, data={"name": "second"})
        self.response_200()
        tag.refresh_from_db()
        self.assertEqual(tag.name, "second")

    def test_detail_partial_update_404(self):
        """Do we generate 404 if tag not found?"""
        url = reverse("api-tag-detail", slug="nonexistent")
        self.patch(url, data={"name": "second"})
        self.response_404()

    def test_detail_delete(self):
        """Can we delete a tag?"""
        tag = TagFactory()
        self.delete("api-tag-detail", slug=tag.slug)
        self.response_204()
        self.assertFalse(
            Tag.objects.filter(pk=tag.pk).exists()
        )

    def test_detail_delete_404(self):
        """Do we generate 404 if tag not found?"""
        self.delete("api-tag-detail", slug="nonexistent")
        self.response_404()


class StartupAPITests(APITestCase):
    """Test API Views for Startup objects"""

    maxDiff = None

    @property
    def response_json(self):
        """Shortcut to obtain JSON from last response"""
        return json.loads(self.last_response.content)

    def test_list(self):
        """Is there a list of Startup objects"""
        url_name = "api-startup-list"
        startup_list = StartupFactory.create_batch(10)
        self.get_check_200(url_name)
        self.assertCountEqual(
            self.response_json,
            StartupSerializer(
                startup_list,
                many=True,
                **context_kwarg(reverse(url_name))
            ).data,
        )

    def test_list_empty(self):
        """Do we return an empty list if no startups?"""
        self.get_check_200("api-startup-list")
        self.assertEquals(self.response_json, [])

    def test_list_create(self):
        """Does Startup list view create new objects via POST?"""
        self.assertEqual(Startup.objects.count(), 0)
        self.post(
            "api-startup-list",
            data=get_instance_data(StartupFactory.build()),
        )
        self.response_201()
        self.assertEqual(Startup.objects.count(), 1)

    def test_detail(self):
        """Is there a detail view for a Startup object"""
        startup = StartupFactory()
        url = reverse(
            "api-startup-detail", slug=startup.slug
        )
        self.get_check_200(url)
        self.assertCountEqual(
            self.response_json,
            StartupSerializer(
                startup, **context_kwarg(url)
            ).data,
        )

    def test_detail_404(self):
        """Do we generate 404 if startup not found?"""
        self.get("api-startup-detail", pk=1)
        self.response_404()

    def test_detail_update(self):
        """Can we update a Startup via PUT?"""
        startup = StartupFactory(name="first")
        url = reverse(
            "api-startup-detail", slug=startup.slug
        )
        self.put(
            url,
            data={
                **get_instance_data(startup),
                "name": "second",
            },
        )
        self.response_200()
        startup.refresh_from_db()
        self.assertEqual(startup.name, "second")

    def test_detail_update_404(self):
        """Do we generate 404 if startup not found?"""
        url = reverse(
            "api-startup-detail", slug="nonexistent"
        )
        self.put(
            url,
            data=get_instance_data(StartupFactory.build()),
        )
        self.response_404()

    def test_detail_partial_update(self):
        """Can we update a Startup via PATCH?"""
        startup = StartupFactory(name="first")
        url = reverse(
            "api-startup-detail", slug=startup.slug
        )
        self.patch(url, data={"name": "second"})
        self.response_200()
        startup.refresh_from_db()
        self.assertEqual(startup.name, "second")

    def test_detail_partial_update_404(self):
        """Do we generate 404 if startup not found?"""
        url = reverse(
            "api-startup-detail", slug="nonexistent"
        )
        self.patch(url, data={"name": "second"})
        self.response_404()

    def test_detail_delete(self):
        """Can we delete a startup?"""
        startup = StartupFactory()
        self.delete("api-startup-detail", slug=startup.slug)
        self.response_204()
        self.assertFalse(
            Startup.objects.filter(pk=startup.pk).exists()
        )

    def test_detail_delete_404(self):
        """Do we generate 404 if startup not found?"""
        self.delete(
            "api-startup-detail", slug="nonexistent"
        )
        self.response_404()

    def test_tags_get(self):
        """Can we get the list of tags for a startup?"""
        tags = TagFactory.create_batch(3)
        startup = StartupFactory(tags=tags)
        self.get_check_200(
            "api-startup-tags", slug=startup.slug
        )
        self.assertCountEqual(
            lmap(get_tag_data, tags),
            lmap(omit_url, self.response_json),
        )

    def test_tags_post_single(self):
        """Can we relate an existing tag to a Startup?"""
        tags = TagFactory.create_batch(2)
        startup = StartupFactory(tags=tags)
        new_tag_data = get_tag_data(TagFactory())
        self.post(
            "api-startup-tags",
            slug=startup.slug,
            data=new_tag_data,
        )
        self.response_204()
        startup.refresh_from_db()
        related_tag_data = lmap(
            get_tag_data, startup.tags.all()
        )
        self.assertEqual(len(related_tag_data), 3)
        self.assertIn(new_tag_data, related_tag_data)

    def test_tags_post_tag_not_found(self):
        """Do we provide an error if the Tag doesn't exist?"""
        tags = TagFactory.create_batch(2)
        startup = StartupFactory(tags=tags)
        unsaved_tag_data = get_tag_data(TagFactory.build())
        self.post(
            "api-startup-tags",
            slug=startup.slug,
            data=unsaved_tag_data,
        )
        self.response_404()

    def test_tags_options(self):
        """Can we see OPTIONS on the Startup's Tag action?"""
        startup = StartupFactory()
        self.options("api-startup-tags", slug=startup.slug)
        self.response_200()

    def test_tags_put_patch_delete(self):
        """Do we disallow unsupported methods with 405 errors?"""
        tags = TagFactory.create_batch(2)
        startup = StartupFactory(tags=tags)
        new_tag_data = get_tag_data(TagFactory())
        url_kwargs = {
            "url_name": "api-startup-tags",
            "slug": startup.slug,
            "data": new_tag_data,
        }
        self.put(**url_kwargs)
        self.response_405()
        self.patch(**url_kwargs)
        self.response_405()
        self.delete("api-startup-tags", slug=startup.slug)
        self.response_405()


class NewsLinkAPITests(APITestCase):
    """Test API Views for NewsLink objects"""

    maxDiff = None

    @property
    def response_json(self):
        """Shortcut to obtain JSON from last response"""
        return json.loads(self.last_response.content)

    def test_list(self):
        """Is there a list of NewsLink objects"""
        url_name = "api-newslink-list"
        newslink_list = NewsLinkFactory.create_batch(10)
        self.get_check_200(url_name)
        self.assertCountEqual(
            self.response_json,
            NewsLinkSerializer(
                newslink_list,
                many=True,
                **context_kwarg(reverse(url_name))
            ).data,
        )

    def test_list_empty(self):
        """Do we return an empty list if no articles?"""
        self.get_check_200("api-newslink-list")
        self.assertEquals(self.response_json, [])

    def test_list_create(self):
        """Can articles be created by POST?"""
        startup = StartupFactory()
        newslink = NewsLinkFactory.build()
        nl_num = NewsLink.objects.count()
        self.post(
            "api-newslink-list",
            data={
                **get_instance_data(newslink),
                "startup": reverse(
                    "api-startup-detail",
                    slug=startup.slug,
                    full=True,
                ),
            },
        )
        self.assertEqual(
            nl_num + 1, NewsLink.objects.count()
        )
        self.assertTrue(
            NewsLink.objects.filter(
                slug=newslink.slug, startup=startup
            ).exists()
        )

    def test_detail(self):
        """Is there a detail view for a NewsLink object"""
        newslink = NewsLinkFactory()
        url = reverse(
            "api-newslink-detail",
            startup_slug=newslink.startup.slug,
            newslink_slug=newslink.slug,
        )
        self.get_check_200(url)
        self.assertCountEqual(
            self.response_json,
            NewsLinkSerializer(
                newslink, **context_kwarg(url)
            ).data,
        )

    def test_detail_404(self):
        """Do we generate 404 if newslink not found?"""
        self.get(
            "api-newslink-detail",
            startup_slug="django",
            newslink_slug="the-best",
        )
        self.response_404()

    def test_detail_update(self):
        """Can we update an article via PUT?"""
        newslink = NewsLinkFactory(title="first")
        self.put(
            "api-newslink-detail",
            startup_slug=newslink.startup.slug,
            newslink_slug=newslink.slug,
            data={
                **get_instance_data(newslink),
                "title": "second",
                "startup": reverse(
                    "api-startup-detail",
                    slug=newslink.startup.slug,
                    full=True,
                ),
            },
        )
        self.response_200()
        newslink.refresh_from_db()
        self.assertEqual(newslink.title, "second")

    def test_detail_update_404(self):
        """Do we generate 404 if newslink not found?"""
        self.put(
            "api-newslink-detail",
            startup_slug="django",
            newslink_slug="the-best",
            data={"title": "second"},
        )
        self.response_404()

    def test_detail_partial_update(self):
        """Can we update an article via PATCH?"""
        newslink = NewsLinkFactory(title="first")
        self.patch(
            "api-newslink-detail",
            startup_slug=newslink.startup.slug,
            newslink_slug=newslink.slug,
            data={"title": "second"},
        )
        self.response_200()
        newslink.refresh_from_db()
        self.assertEqual(newslink.title, "second")

    def test_detail_partial_update_404(self):
        """Do we generate 404 if article not found?"""
        self.patch(
            "api-newslink-detail",
            startup_slug="django",
            newslink_slug="the-best",
            data={"title": "second"},
        )
        self.response_404()

    def test_detail_delete(self):
        """Can we delete an article?"""
        newslink = NewsLinkFactory()
        self.delete(
            "api-newslink-detail",
            startup_slug=newslink.startup.slug,
            newslink_slug=newslink.slug,
            data={"title": "second"},
        )
        self.response_204()
        self.assertFalse(
            NewsLink.objects.filter(pk=newslink.pk).exists()
        )

    def test_detail_delete_404(self):
        """Do we generate 404 if startup not found?"""
        self.delete(
            "api-newslink-detail",
            startup_slug="django",
            newslink_slug="the-best",
            data={"title": "second"},
        )
        self.response_404()
