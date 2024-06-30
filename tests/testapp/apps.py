from django.apps import AppConfig


class WagtailPagetranslationTestAppConfig(AppConfig):
    label = "testapp"
    name = "tests.testapp"
    verbose_name = "Wagtail pagetranslation tests"
    default_auto_field = "django.db.models.BigAutoField"
