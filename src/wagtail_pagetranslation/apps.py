from django.apps import AppConfig
from django.db import models
from modelcluster.fields import ParentalKey

from wagtail_pagetranslation import settings as pt_settings


class WagtailPagetranslationAppConfig(AppConfig):
    label = "wagtail_pagetranslation"
    name = "wagtail_pagetranslation"
    verbose_name = "Wagtail Page Translation"

    def register_pagetranslation_models(self):
        """
         - Dynamically creates translation{modelname} table for every page type
        that uses TranslationMixin
         - Dynamically copies page fields into trasnlation model that are listed
         in the translatable_fields attribute of the TranslationMixin
         - Dynamcally adds 'Translation' tab to the wagtail admin edit interface
         of the page type that uses TranslationMixin
        """
        from wagtail.admin.panels import FieldPanel
        from wagtail.models import get_page_models

        from wagtail_pagetranslation.translation import (
            TranslationMixin,
            TranslationsInlinePanel,
        )

        for page_model in get_page_models():
            if not issubclass(page_model, TranslationMixin):
                continue
            model_name = page_model._meta.model_name
            app_label = page_model._meta.app_label
            relation_name = f"{page_model._meta.model_name}_translations"
            translation_model_name = f"translation{model_name}"

            fields = {
                "page": ParentalKey(
                    "wagtailcore.Page",
                    on_delete=models.CASCADE,
                    related_name=relation_name,
                ),
                "language": models.CharField(
                    choices=pt_settings.TRANSLATABLE_LANGUAGES,
                    max_length=8,
                    help_text="",
                    default="",
                ),
            }
            panels = [FieldPanel("language")]
            for field_name in page_model.translatable_fields:
                original_field = page_model._meta.get_field(field_name)

                fields[field_name] = original_field.clone()

                panels.append(FieldPanel(field_name))

            type(
                translation_model_name,
                (models.Model,),
                {
                    **fields,
                    "Meta": type(
                        "Meta",
                        (),
                        {
                            "app_label": app_label,
                            "unique_together": [["page", "language"]],
                        },
                    ),
                    "__module__": page_model.__module__,
                    "panels": panels,
                },
            )

            page_model.translation_panels = [TranslationsInlinePanel(relation_name)]

    def ready(self):
        self.register_pagetranslation_models()
