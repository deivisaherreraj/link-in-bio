from operator import ne

import reflex as rx

from website_frontend.components.status_badge import status_badge
from website_frontend.model.featured import Featured
from website_frontend.shared.urls import (
    is_actionable_external_url,
)
from website_frontend.styles.colors import BackgroundColor, BorderColor
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Color, Margin, Padding, Spacing


def _link_href(url: str | None | rx.Var) -> str | rx.Var:
    if hasattr(url, "to"):
        return url.to(str)

    return url or "#"


def _action_link(
    *,
    label: str,
    href: str | None | rx.Var,
    icon: str,
    aria_label: str,
    is_external: bool,
    primary: bool = False,
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.text(label),
            rx.icon(icon, font_size=FontSize.SMALL.value),
            spacing=Spacing.VERY_SMALL.value,
            align="center",
        ),
        href=_link_href(href),
        is_external=is_external,
        font_size=FontSize.SMALL.value,
        font_weight=(
            FontWeight.SEMI_BOLD.value if primary else FontWeight.MEDIUM.value
        ),
        color=Color.WHITE.value,
        display="inline-flex",
        align_items="center",
        gap="0.25rem",
        z_index="10",
        aria_label=aria_label,
        padding_y=Padding.SMALL.value,
        padding_x=Padding.DEFAULT.value,
        border_radius="999px",
        border=(
            f"1px solid {Color.BG_WHITE_TRANSPARENT.value}"
            if primary
            else f"1px solid {BorderColor.WHITE_TRANSPARENT.value}"
        ),
        background_color=(
            BackgroundColor.LIGHT.value if primary else Color.BG_WHITE_TRANSPARENT.value
        ),
        class_name=(
            "transition-all z-10 hover:-translate-y-0.5 "
            "hover:border-white/30 hover:bg-white/10"
        ),
    )


def _icon_action_link(
    *,
    href: str | None | rx.Var,
    icon_class: str,
    aria_label: str,
    is_external: bool,
) -> rx.Component:
    return rx.link(
        rx.el.I.create(
            class_name=icon_class,
            font_size=FontSize.DEFAULT.value,
        ),
        href=_link_href(href),
        is_external=is_external,
        color=Color.WHITE.value,
        display="inline-flex",
        align_items="center",
        justify_content="center",
        width="2.5rem",
        height="2.5rem",
        min_width="2.5rem",
        border_radius="999px",
        border=f"1px solid {BorderColor.WHITE_TRANSPARENT.value}",
        background_color=Color.BG_WHITE_TRANSPARENT.value,
        z_index="10",
        aria_label=aria_label,
        class_name=(
            "transition-all z-10 hover:-translate-y-0.5 "
            "hover:border-white/30 hover:bg-white/10"
        ),
    )


def link_featured(featured: Featured) -> rx.Component:
    return rx.flex(
        rx.hstack(
            rx.heading(
                featured.title,
                font_size=FontSize.LARGE.value,
                font_weight=FontWeight.BOLD.value,
                color=Color.WHITE.value,
                flex="1 1 0%",
                as_="h3",
                line_height="1.2",
                margin_top=Margin.ZERO.value,
                word_break="break-word",
                overflow_wrap="anywhere",
            ),
            status_badge(featured.status),
            align_items="center",
            justify="between",
            width="100%",
            flex_wrap="wrap",
            gap="0.5rem",
        ),
        rx.cond(
            featured.description is not None,
            rx.text(
                featured.description,
                font_size=FontSize.SMALL.value,
                color=Color.WHITE.value,
                opacity="0.78",
                class_name="line-clamp-3",
                line_height="1.55",
                as_="p",
            ),
        ),
        rx.cond(
            featured.technologies != [],
            rx.flex(
                rx.foreach(
                    featured.technologies,
                    lambda tech: rx.text(
                        tech,
                        padding_y="0.2rem",
                        padding_x=Padding.DEFAULT.value,
                        font_size=FontSize.TINY.value,
                        color=Color.WHITE.value,
                        background_color=Color.BG_WHITE_TRANSPARENT.value,
                        border_radius="999px",
                        border=f"1px solid {BorderColor.WHITE_TRANSPARENT.value}",
                        as_="span",
                    ),
                ),
                flex_wrap="wrap",
                gap="0.4rem",
            ),
        ),
        rx.flex(
            rx.cond(
                ne(featured.href, None),
                _action_link(
                    label="Ver Detalles",
                    href=featured.href,
                    icon="arrow-right",
                    aria_label=f"Ver proyecto {featured.title}",
                    is_external=(
                        False
                        if hasattr(featured.href, "to")
                        else is_actionable_external_url(featured.href)
                    ),
                    primary=True,
                ),
            ),
            rx.hstack(
                rx.cond(
                    ne(featured.github_url, None),
                    _icon_action_link(
                        href=featured.github_url,
                        icon_class="fa-brands fa-github",
                        aria_label="Ver código en GitHub",
                        is_external=True,
                    ),
                ),
                rx.cond(
                    ne(featured.live_url, None),
                    _icon_action_link(
                        href=featured.live_url,
                        icon_class="fa-solid fa-arrow-up-right-from-square",
                        aria_label="Ver proyecto en vivo",
                        is_external=True,
                    ),
                ),
                spacing=Spacing.VERY_SMALL.value,
                z_index="10",
                flex_shrink="0",
            ),
            justify="between",
            align="center",
            flex_wrap="wrap",
            width="100%",
            gap="0.75rem",
            margin_top="auto",
            padding_top=Padding.SMALL.value,
        ),
        direction="column",
        justify="end",
        spacing=Spacing.SMALL.value,
        width="100%",
        height="100%",
        padding=Padding.ZERO.value,
    )
