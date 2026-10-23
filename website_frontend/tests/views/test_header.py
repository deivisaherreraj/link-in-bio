from website_frontend.model.profile import ProfileBioSegment
from website_frontend.views.header import (
    _intro_paragraph,
    _render_intro_segment,
    header,
)


def test_header_renders_profile_bio_short_below_live_banner() -> None:
    rendered = str(header())

    assert '["bio_short_segments"]' in rendered


def test_intro_paragraph_reads_from_profile_contract() -> None:
    rendered = str(_intro_paragraph())

    assert '["bio_short_segments"]' in rendered


def test_render_intro_segment_emphasizes_highlighted_phrases() -> None:
    rendered = str(
        _render_intro_segment(
            ProfileBioSegment(text="desarrollador Full-Stack", is_highlighted=True)
        )
    )

    assert "strong" in rendered.lower()
    assert "desarrollador Full-Stack" in rendered
