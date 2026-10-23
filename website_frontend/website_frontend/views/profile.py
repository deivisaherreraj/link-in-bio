import reflex as rx

from website_frontend.components.avatar_with_status import avatar_with_status
from website_frontend.components.tech_badge import tech_badge
from website_frontend.model.avatar_status import AvatarStatus
from website_frontend.model.primary_social import PrimarySocial
from website_frontend.state.page_state import PageState
from website_frontend.styles.colors import Color, TextColor
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Size, Spacing


def profile(
    name: str,
    handle: str,
    headline: str,
    tech_stack_summary: str,
    avatar_url: str,
    avatar_status: AvatarStatus,
    github_url: str | None = None,
    linkedin_url: str | None = None,
    email: str | None = None,
) -> rx.Component:
    def social_icon(link: PrimarySocial) -> rx.Component:
        return rx.cond(
            link.is_active,
            rx.link(
                rx.el.I.create(
                    class_name=link.icon,
                    font_size=FontSize.EXTRA_LARGE.value,
                ),
                href=link.url,
                is_external=rx.cond(link.url.startswith("mailto:"), False, True),
                aria_label=link.label,
                color=TextColor.BODY.value,
                _hover={"color": Color.PRIMARY.value},
            ),
        )

    static_social_links: list[rx.Component] = []

    if isinstance(github_url, str) and github_url.strip():
        static_social_links.append(
            rx.link(
                rx.el.I.create(
                    class_name="fa-brands fa-github",
                    font_size=FontSize.EXTRA_LARGE.value,
                ),
                href=github_url.strip(),
                is_external=True,
                aria_label="GitHub",
                color=TextColor.BODY.value,
                _hover={"color": Color.PRIMARY.value},
            )
        )

    if isinstance(linkedin_url, str) and linkedin_url.strip():
        static_social_links.append(
            rx.link(
                rx.el.I.create(
                    class_name="fa-brands fa-linkedin",
                    font_size=FontSize.EXTRA_LARGE.value,
                ),
                href=linkedin_url.strip(),
                is_external=True,
                aria_label="LinkedIn",
                color=TextColor.BODY.value,
                _hover={"color": Color.PRIMARY.value},
            )
        )

    if isinstance(email, str) and email.strip():
        static_social_links.append(
            rx.link(
                rx.el.I.create(
                    class_name="fa-regular fa-envelope",
                    font_size=FontSize.EXTRA_LARGE.value,
                ),
                href=f"mailto:{email.strip()}",
                is_external=False,
                aria_label="Email",
                color=TextColor.BODY.value,
                _hover={"color": Color.PRIMARY.value},
            )
        )

    return rx.vstack(
        # Avatar con badge de disponibilidad
        avatar_with_status(
            avatar_url=avatar_url,
            name=name,
            status=avatar_status,
        ),
        # Nombre con posibilidad de gradiente (via CSS)
        rx.heading(
            name,
            color=Color.TRANSPARENT.value,
            font_weight=FontWeight.BOLD.value,
            font_size=FontSize.EXTRA_LARGE.value,
            margin_bottom=Size.VERY_SMALL.value,
            class_name="profile-name-gradient",
            as_="h1",
        ),
        # Handle
        rx.text(
            handle,
            color=Color.PRIMARY.value,
            font_weight=FontWeight.MEDIUM.value,
            margin_bottom=Size.SMALL.value,
        ),
        # Tagline
        rx.text(
            headline,
            color=Color.WHITE.value,
            font_size=FontSize.MEDIUM.value,
            font_weight=FontWeight.MEDIUM.value,
            margin_bottom=Size.VERY_SMALL.value,
        ),
        # Tech stack description
        rx.text(
            tech_stack_summary,
            color=Color.GRAY.value,
            font_size=FontSize.SMALL.value,
            as_="p",
        ),
        # Tecnologías (badges)
        rx.flex(
            rx.foreach(PageState.technologies, tech_badge),
            gap="0.75rem",
            wrap="wrap",
            justify_content="center",
            spacing=Spacing.SMALL.value,
            margin_top=Size.SMALL.value,
            margin_bottom=Size.DEFAULT.value,
        ),
        # Iconos sociales
        rx.hstack(
            *static_social_links,
            *(
                []
                if static_social_links
                else [rx.foreach(PageState.profile_info.primary_socials, social_icon)]
            ),
            justify="center",
            spacing=Spacing.LARGE.value,
            width="100%",
        ),
        align_items="center",
        text_align="center",
        flex_direction="column",
        display="flex",
        width="100%",
        spacing=Spacing.ZERO.value,
        on_mount=PageState.init_technologies,
    )
