from wagtail.admin.panels import InlinePanel, ObjectList, TabbedInterface
from wagtail.utils.decorators import cached_classmethod


class TranslationsInlinePanel(InlinePanel):
    class BoundPanel(InlinePanel.BoundPanel):
        template_name = "translations_inline_panel.html"

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # copy initial value for field form model and use it in translation form
            fields = {}
            for field in self.instance.translatable_fields:
                fields[field] = getattr(self.instance, field)
            self.empty_child.form.initial = fields


class TranslationMixin:
    """
    This mixin should be added to custom page type before Page class:

    class HomePage(TranslationMixin, Page):
        # list of fields that should have translation
        translatable_fields = ["title", ...]
    """

    translatable_fields = ["title"]
    translation_panels = []

    def get_language(self, request):
        return request.GET.get("lang")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        lang = self.get_language(request)
        if not lang:
            return context

        translation_manager = getattr(self, f"{self._meta.model_name}_translations")
        translation_model = translation_manager.model
        if not translation_model:
            return context

        try:
            translation = translation_model.objects.get(language=lang)
        except translation_model.DoesNotExist:
            translation = None
        if translation:
            for field_name in self.translatable_fields:
                setattr(self, field_name, getattr(translation, field_name))

        return context

    @cached_classmethod
    def get_edit_handler(self):
        # add new translation tab to pages with translations mixin
        edit_handler = TabbedInterface(
            super().get_edit_handler().children
            + [
                ObjectList(self.translation_panels, heading="Translations"),
            ]
        )

        return edit_handler.bind_to_model(self)
