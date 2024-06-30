import json

import pytest

from django.apps import apps
from wagtail.models import Page

from tests.testapp.models import BlogPage


blog_en_body = json.dumps(
    [
        {
            "type": "text",
            "value": """Simple text""",
        },
        {
            "type": "paragraph",
            "value": """RichText text""",
        },
    ]
)

blog_nl_body = json.dumps(
    [
        {
            "type": "text",
            "value": """Eenvoudige tekst""",
        },
        {
            "type": "paragraph",
            "value": """RichText tekst""",
        },
    ]
)


@pytest.fixture
def translation_nl():
    TranslationModel = apps.get_model("testapp.translationblogpage")
    translation = TranslationModel(
        language="nl",
        title="Blog Titel",
        intro="Blog introduction",
        body=blog_nl_body,
    )
    return translation


@pytest.fixture
def blog_page_1(translation_nl):
    blog_page = BlogPage(
        slug="blog",
        title="Blog Title",
        intro="Blog introduction",
        body=blog_en_body,
        live=True,
        first_published_at="2024-07-29 00:00:00+01:00",
    )
    homepage = Page.get_first_root_node().get_children()[0]
    homepage.add_child(instance=blog_page)
    blog_page.blogpage_translations.add(translation_nl)
    blog_page.save()
    return blog_page
