import pytest

from django.apps import apps


pytestmark = pytest.mark.django_db


def test_translation_model_created():
    # get_model throws error when model does not exist
    model = apps.get_model("testapp.translationblogpage")
    assert model.__name__ == "translationblogpage"
