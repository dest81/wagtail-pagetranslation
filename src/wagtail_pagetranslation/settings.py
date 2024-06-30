from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


DEFAULT_LANGUAGE = getattr(settings, "WAGTAIL_PAGETRANSLATION_DEFAULT_LANGUAGE", None)
if not DEFAULT_LANGUAGE:
    raise ImproperlyConfigured(
        "WAGTAIL_PAGETRANSLATION_DEFAULT_LANGUAGE is not set in the setting."
    )

AVAILABLE_LANGUAGES = getattr(
    settings,
    "WAGTAIL_PAGETRANSLATION_LANGUAGES",
    settings.LANGUAGES,
)


TRANSLATABLE_LANGUAGES = [
    (val, label) for val, label in AVAILABLE_LANGUAGES if val != DEFAULT_LANGUAGE
]
