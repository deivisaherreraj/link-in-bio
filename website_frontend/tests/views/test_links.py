import inspect

from website_frontend.model.social_link import SocialLink
from website_frontend.styles.styles import Color
from website_frontend.views.links import (
    featured_section_content,
    links,
    render_social_link,
)


def test_render_social_link_uses_model_contract_fields() -> None:
    component = render_social_link(
        SocialLink(
            label="Email",
            url="mailto:test@example.com",
            icon="fa-solid fa-envelope",
            section="contact",
            priority=1,
            is_active=True,
            is_external=False,
            description="Direct contact",
            badge="Correo",
            border_color="#123456",
        )
    )

    rendered = str(component)

    assert "mailto:test@example.com" in rendered
    assert "Direct contact" in rendered
    assert "fa-solid fa-envelope" in rendered
    assert "1px solid #123456" in rendered
    assert '"padding" : "12px"' in rendered or '["padding"] : "12px"' in rendered
    assert 'target:(false ? "_blank" : "")' in rendered


def test_render_social_link_visually_separates_disabled_cards() -> None:
    component = render_social_link(
        SocialLink(
            label="Próximamente",
            url="https://example.com/soon",
            icon="fa-solid fa-hourglass-half",
            section="resources",
            priority=99,
            is_active=False,
            is_external=True,
            description="Aún no disponible.",
        )
    )

    rendered = str(component)

    assert '(false ? "1" : "0.74")' in rendered
    assert "Pr" in rendered
    assert "\\u00f3ximamente" in rendered
    assert "grayscale(0.1) saturate(0.75)" in rendered
    assert "1px dashed #ffffff26" in rendered


def test_render_social_link_uses_brand_colors_for_community_icons() -> None:
    component = render_social_link(
        SocialLink(
            label="Discord",
            url="https://discord.gg/example",
            icon="fa-brands fa-discord",
            section="community",
            priority=1,
            is_active=True,
            is_external=True,
        )
    )

    rendered = str(component)

    assert Color.DISCORD.value in rendered


def test_links_view_loads_featured_and_social_link_state_on_mount() -> None:
    rendered = inspect.getsource(links)

    assert "featured_links" in rendered
    assert "load_social_links" in rendered


def test_featured_section_content_renders_single_item_once_without_carousel() -> None:
    rendered = inspect.getsource(featured_section_content)

    assert "rx.foreach(featured_projects, _render_featured_card)" in rendered


def test_featured_section_content_keeps_carousel_for_multiple_items() -> None:
    rendered = inspect.getsource(links)

    assert "featured_section_content(" in rendered
    assert "use_carousel=PageState.has_multiple_featured_projects" in rendered
