"""
Placeholder test, so that pytest doesn't fail with an empty testsuite. Feel free to
remove this when you start writing tests.
https://github.com/pytest-dev/pytest/issues/2393
"""

import pytest


pytestmark = pytest.mark.django_db


def test_blog_page_default_translation(client, blog_page_1):
    resp = client.get("/blog/")
    assert resp.status_code == 200
    assert "Blog Title" in resp.rendered_content
    assert "Blog introduction" in resp.rendered_content
    assert "Simple text" in resp.rendered_content
    assert "RichText text" in resp.rendered_content


def test_blog_page_nl_translation(client, blog_page_1, translation_nl):
    resp = client.get("/blog/?lang=nl")
    assert resp.status_code == 200
    assert "Blog Titel" in resp.rendered_content
    assert "Blog introduction" in resp.rendered_content
    assert "Eenvoudige tekst" in resp.rendered_content
    assert "RichText tekst" in resp.rendered_content


def test_blog_page_no_translation(client, blog_page_1, translation_nl):
    resp = client.get("/blog/?lang=de")
    assert resp.status_code == 200
    assert "Blog Title" in resp.rendered_content
    assert "Blog introduction" in resp.rendered_content
    assert "Simple text" in resp.rendered_content
    assert "RichText text" in resp.rendered_content
