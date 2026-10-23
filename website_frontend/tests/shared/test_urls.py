from website_frontend.shared.urls import (
    is_actionable_external_url,
    is_actionable_href,
)


def test_is_actionable_href_rejects_empty_and_placeholders() -> None:
    assert is_actionable_href(None) is False
    assert is_actionable_href("") is False
    assert is_actionable_href("   ") is False
    assert is_actionable_href("/") is False
    assert is_actionable_href("#") is False


def test_is_actionable_href_accepts_non_placeholder_internal_and_external_urls() -> (
    None
):
    assert is_actionable_href("/projects") is True
    assert is_actionable_href("https://example.com") is True


def test_is_actionable_external_url_rejects_invalid_or_non_http_urls() -> None:
    assert is_actionable_external_url(None) is False
    assert is_actionable_external_url("not-a-url") is False
    assert is_actionable_external_url("javascript:alert('xss')") is False
    assert is_actionable_external_url("/projects") is False


def test_is_actionable_external_url_accepts_http_urls() -> None:
    assert is_actionable_external_url("https://example.com") is True
    assert is_actionable_external_url(" http://example.com/path ") is True
