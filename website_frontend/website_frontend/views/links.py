from operator import ne

import reflex as rx
from reflex.components.lucide import Icon

from website_frontend.components.link_featured import link_featured
from website_frontend.components.section import section
from website_frontend.components.ui.auto_scrolling_carousel import (
    auto_scrolling_carousel,
)
from website_frontend.components.ui.direction_aware_hover import (
    direction_aware_hover,
)
from website_frontend.model.social_link import SocialLink
from website_frontend.state.page_state import PageState
from website_frontend.styles.colors import BackgroundColor, BorderColor
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Color, Margin, Padding, Spacing


def _fallback_icon_color(label: str) -> str | None:
    normalized_label = label.strip().lower()

    if "discord" in normalized_label:
        return Color.DISCORD.value

    if "youtube" in normalized_label:
        return Color.RED.value

    if "twitch" in normalized_label:
        return Color.PURPLE.value

    return None


def render_social_link(link: SocialLink) -> rx.Component:
    icon_color = (
        link.icon_color or _fallback_icon_color(link.label)
        if isinstance(link, SocialLink)
        else rx.cond(
            ne(link.icon_color, None),
            link.icon_color,
            rx.cond(
                link.label == "Discord",
                Color.DISCORD.value,
                rx.cond(
                    link.label == "YouTube",
                    Color.RED.value,
                    rx.cond(
                        link.label == "Twitch",
                        Color.PURPLE.value,
                        Color.WHITE.value,
                    ),
                ),
            ),
        )
    )

    return rx.link(
        rx.hstack(
            rx.box(
                rx.el.I.create(
                    class_name=link.icon,
                    style={"color": icon_color},
                ),
                font_size=FontSize.DEFAULT.value,
                color=icon_color,
                width="32px",
                height="32px",
                min_width="32px",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink=0,
                border_radius="8px",
                background_color=BackgroundColor.LIGHT.value,
                border=f"1px solid {Color.BG_WHITE_TRANSPARENT.value}",
            ),
            rx.box(
                rx.hstack(
                    rx.text(
                        link.label,
                        color=Color.WHITE.value,
                        font_weight=FontWeight.SEMI_BOLD.value,
                        font_size=FontSize.MEDIUM.value,
                        as_="span",
                        line_height="1.2",
                    ),
                    rx.cond(
                        ne(link.badge, None),
                        rx.text(
                            link.badge,
                            font_size=FontSize.TINY.value,
                            font_weight=FontWeight.MEDIUM.value,
                            color=Color.WHITE.value,
                            padding_y=Padding.SMALL.value,
                            padding_x=Padding.MEDIUM.value,
                            border_radius="999px",
                            line_height="1",
                            text_transform="uppercase",
                            letter_spacing="0.02em",
                            white_space="nowrap",
                            background_color=rx.cond(
                                ne(link.badge_color, None),
                                link.badge_color,
                                rx.cond(
                                    link.is_active,
                                    Color.PRIMARY.value,
                                    Color.GRAY_DARK.value,
                                ),
                            ),
                            border=f"1px solid {Color.BG_WHITE_TRANSPARENT.value}",
                            as_="span",
                        ),
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="flex-start",
                    width="100%",
                    flex_wrap="wrap",
                    gap="8px",
                    margin_bottom=Margin.VERY_SMALL.value,
                ),
                rx.text(
                    rx.cond(ne(link.description, None), link.description, ""),
                    font_size=FontSize.TINY.value,
                    color=Color.GRAY.value,
                    as_="span",
                    line_height="1.45",
                    class_name="line-clamp-2",
                ),
                flex_grow=1,
                flex_shrink=1,
                flex_basis="0%",
                display="flex",
                flex_direction="column",
                justify_content="center",
                text_align="left",
            ),
            rx.box(
                Icon.create(
                    "chevron-right",
                    size=18,
                    color=Color.GRAY.value,
                ),
                display="flex",
                align_items="center",
                justify_content="center",
                align_self="center",
                flex_shrink=0,
                padding_left=Padding.SMALL.value,
            ),
            align="center",
            justify="between",
            spacing=Spacing.EXTRA_SMALL.value,
            width="100%",
            min_height="100%",
        ),
        href=rx.cond(link.is_active, link.url, "#"),
        is_external=link.is_external,
        width="100%",
        display="flex",
        align_items="center",
        justify_content="center",
        text_decoration="none",
        opacity=rx.cond(link.is_active, "1", "0.74"),
        filter=rx.cond(link.is_active, "none", "grayscale(0.1) saturate(0.75)"),
        pointer_events=rx.cond(link.is_active, "auto", "none"),
        padding="12px",
        border_radius="12px",
        min_height="84px",
        background=rx.cond(
            link.is_active,
            BackgroundColor.SURFACE.value,
            "linear-gradient(180deg, rgba(14, 20, 28, 0.98) 0%, "
            "rgba(9, 13, 18, 1) 100%)",
        ),
        box_shadow=rx.cond(
            ne(link.border_color, None),
            f"0 0 0 1px {Color.WHITE_TRANSPARENT.value}, "
            "0 14px 32px rgba(0, 0, 0, 0.28)",
            "0 12px 28px rgba(0, 0, 0, 0.2)",
        ),
        border=rx.cond(
            ne(link.border_color, None),
            f"1px solid {link.border_color}",
            rx.cond(
                link.is_active,
                f"1px solid {BorderColor.DEFAULT.value}",
                f"1px dashed {BorderColor.WHITE_TRANSPARENT.value}",
            ),
        ),
        transition=(
            "transform 180ms ease, box-shadow 180ms ease, "
            "border-color 180ms ease, background 180ms ease"
        ),
        _hover=rx.cond(
            link.is_active,
            {
                "transform": "translateY(-2px)",
                "background": BackgroundColor.SURFACE_HOVER.value,
                "boxShadow": "0 16px 32px rgba(0, 0, 0, 0.24)",
                "borderColor": rx.cond(
                    ne(link.border_color, None),
                    link.border_color,
                    BorderColor.WHITE_TRANSPARENT.value,
                ),
            },
            {},
        ),
    )


def _render_featured_card(featured) -> rx.Component:
    return rx.flex(
        direction_aware_hover(
            image_url=featured.image_url,
            children=link_featured(featured),
        ),
        width="360px",
        height="288px",
        align_items="center",
        justify_content="center",
    )


def featured_section_content(
    featured_projects: list, use_carousel: bool | rx.Var
) -> rx.Component:
    return rx.cond(
        use_carousel,
        auto_scrolling_carousel(
            reactive_list=featured_projects,
            render_function=_render_featured_card,
            direction="right",
            speed="fast",
        ),
        rx.foreach(featured_projects, _render_featured_card),
    )


def links() -> rx.Component:
    return rx.vstack(
        rx.cond(
            PageState.featured_info,
            section(
                "Proyectos Destacados",
                featured_section_content(
                    featured_projects=PageState.featured_info,
                    use_carousel=PageState.has_multiple_featured_projects,
                ),
            ),
        ),
        section(
            "Plataformas de trabajo",
            rx.foreach(PageState.work_social_links, render_social_link),
        ),
        section(
            "Comunidad",
            rx.foreach(PageState.community_social_links, render_social_link),
        ),
        section(
            "Recursos y más",
            rx.foreach(PageState.resources_social_links, render_social_link),
        ),
        section(
            "Contacto",
            rx.foreach(PageState.contact_social_links, render_social_link),
        ),
        width="100%",
        spacing=Spacing.DEFAULT.value,
        on_mount=[PageState.featured_links, PageState.load_social_links],
    )
