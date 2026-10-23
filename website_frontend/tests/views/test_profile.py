from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.views.profile import profile


def _avatar_status() -> AvatarStatus:
    return AvatarStatus(
        key="activo",
        text="Disponible",
        class_name="is-active",
        icon="fa-bolt",
    )


def test_profile_email_link_is_not_opened_as_external_tab() -> None:
    component = profile(
        name="Deivis",
        handle="@dherrerajdev",
        headline="Tagline",
        tech_stack_summary="Stack",
        avatar_url="/avatar.jpeg",
        avatar_status=_avatar_status(),
        email="test@example.com",
    )

    rendered = str(component)

    assert 'to:"mailto:test@example.com"' in rendered
    assert 'target:(false ? "_blank" : "")' in rendered


def test_profile_external_social_links_keep_external_target() -> None:
    component = profile(
        name="Deivis",
        handle="@dherrerajdev",
        headline="Tagline",
        tech_stack_summary="Stack",
        avatar_url="/avatar.jpeg",
        avatar_status=_avatar_status(),
        github_url="https://github.com/example",
        linkedin_url="https://linkedin.com/in/example",
    )

    rendered = str(component)

    assert 'to:"https://github.com/example"' in rendered
    assert 'to:"https://linkedin.com/in/example"' in rendered
    assert 'target:(true ? "_blank" : "")' in rendered


def test_profile_hides_blank_social_links() -> None:
    component = profile(
        name="Deivis",
        handle="@dherrerajdev",
        headline="Tagline",
        tech_stack_summary="Stack",
        avatar_url="/avatar.jpeg",
        avatar_status=_avatar_status(),
        github_url=" ",
        linkedin_url="",
        email="test@example.com",
    )

    rendered = str(component)

    assert 'to:"mailto:test@example.com"' in rendered
    assert 'aria-label":"GitHub"' not in rendered
    assert 'aria-label":"LinkedIn"' not in rendered


def test_profile_keeps_social_icons_below_technology_badges() -> None:
    component = profile(
        name="Deivis",
        handle="@dherrerajdev",
        headline="Tagline",
        tech_stack_summary="Stack",
        avatar_url="/avatar.jpeg",
        avatar_status=_avatar_status(),
        github_url="https://github.com/example",
    )

    rendered = str(component)

    assert "Stack" in rendered
    assert "GitHub" in rendered
    assert 'line_height="1.8"' not in rendered
