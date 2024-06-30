from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from wagtail_pagetranslation.translation import TranslationMixin


class HomePage(Page):
    pass


class BlogPage(TranslationMixin, Page):
    intro = RichTextField(blank=True)
    publication_date = models.DateField(null=True, blank=True)
    body = StreamField(
        [
            ("text", blocks.CharBlock()),
            ("paragraph", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )

    translatable_fields = ["title", "intro", "body"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("publication_date"),
        FieldPanel("body"),
    ]
