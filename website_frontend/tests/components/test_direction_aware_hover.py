import reflex as rx

from website_frontend.components.ui.direction_aware_hover import direction_aware_hover


def test_direction_aware_hover_uses_decorative_background_alt() -> None:
    component = direction_aware_hover(
        image_url="/images/example.png",
        children=rx.text("Contenido"),
    )

    rendered = str(component)

    assert 'alt:""' in rendered
    assert 'alt:"Background"' not in rendered
    assert "/images/example.png" in rendered


def test_direction_aware_hover_supports_missing_image_url() -> None:
    component = direction_aware_hover(
        image_url=None,
        children=rx.text("Contenido"),
    )

    rendered = str(component)

    assert "Contenido" in rendered
    assert "/featured-default.svg" in rendered
    assert "linear-gradient(135deg" in rendered
    assert "featured-hover-card" in rendered
    assert "featured-overlay" in rendered
    assert "featured-scrim" in rendered


def test_direction_aware_hover_keeps_native_link_in_overlay() -> None:
    component = direction_aware_hover(
        image_url="/images/example.png",
        children=rx.link("Open project", href="https://example.com/project"),
    )

    rendered = str(component)

    assert "featured-hover-card" in rendered
    assert "featured-overlay" in rendered
    assert 'to:"https://example.com/project"' in rendered
    assert "tabIndex" not in rendered
