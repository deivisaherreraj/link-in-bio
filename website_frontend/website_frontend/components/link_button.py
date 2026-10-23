import reflex as rx

import website_frontend.styles.styles as styles
from website_frontend.shared.urls import is_actionable_href
from website_frontend.styles.colors import BackgroundColor, Color
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Margin, Padding, Size, Spacing


def link_button(
    href: str,
    title: str,
    description: str | None | rx.Var[str | None],
    image: str | None = None,
    icon: str | None = None,
    icon_color: str | None = None,
    badge: str | None = None,
    badge_color: str = Color.PRIMARY.value,
    border_color: str | None = None,
    is_disabled: bool = False,
    is_external: bool = True,
    animated: bool = False,
) -> rx.Component:
    class_name = ""
    transparent_border = f"1px solid {Color.BG_WHITE_TRANSPARENT.value}"

    # Animación opcional (animate.css)
    if animated:
        class_name = f"{class_name} {styles.BOUNCEIN_ANIMATION}"

    style: dict[str, str] = {
        "padding": "18px 14px",
        "marginBottom": Margin.ZERO.value,
        "borderRadius": "18px",
        "minHeight": "96px",
        "background": (
            "linear-gradient(180deg, rgba(255,255,255,0.08) 0%, "
            "rgba(255,255,255,0.05) 100%)"
        ),
        "boxShadow": "0 18px 44px rgba(0, 0, 0, 0.22)",
        "transition": (
            "transform 180ms ease, box-shadow 180ms ease, "
            "border-color 180ms ease, background 180ms ease"
        ),
    }

    if is_disabled:
        style.update(
            {
                "pointerEvents": "none",
                "opacity": "0.6",
            }
        )

    if border_color is not None:
        style.update(
            {
                "borderColor": border_color,
                "border": f"2px solid {border_color}",
                "boxShadow": f"0 18px 45px {Color.WHITE_TRANSPARENT.value}",
            }
        )

    is_actionable = is_actionable_href(href)
    is_interactive = not is_disabled and is_actionable

    if not is_actionable:
        style.update(
            {
                "pointerEvents": "none",
                "opacity": "0.6",
            }
        )

    on_click = (
        None if not is_interactive else rx.redirect(path=href, is_external=is_external)
    )
    has_visual = bool(icon or image)

    return rx.button(
        rx.hstack(
            rx.cond(
                has_visual,
                rx.box(
                    rx.cond(
                        icon,
                        rx.el.I.create(
                            class_name=icon,
                            style={"color": icon_color} if icon_color else None,
                        ),
                        rx.image(
                            src=image,
                            width=Size.LARGE.value,
                            height=Size.LARGE.value,
                            margin=Size.MEDIUM.value,
                            alt=title,
                        ),
                    ),
                    font_size=FontSize.DEFAULT.value,
                    color=Color.WHITE.value,
                    width="44px",
                    height="44px",
                    min_width="44px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink=0,
                    border_radius="14px",
                    background_color=BackgroundColor.LIGHT.value,
                    border=f"1px solid {Color.BG_WHITE_TRANSPARENT.value}",
                ),
            ),
            rx.box(
                rx.hstack(
                    rx.text(
                        title,
                        color=Color.WHITE.value,
                        font_weight=FontWeight.SEMI_BOLD.value,
                        font_size=FontSize.MEDIUM.value,
                        as_="span",
                        line_height="1.2",
                    ),
                    rx.cond(
                        badge,
                        rx.text(
                            badge,
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
                            style={
                                "backgroundColor": badge_color,
                                "border": transparent_border,
                            }
                            if badge_color
                            else {"border": transparent_border},
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
                    description,
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
                text_align="left",
            ),
            rx.box(
                rx.icon(
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
            align="start",
            spacing=Spacing.SMALL.value,
            width="100%",
        ),
        disabled=is_disabled or not is_actionable,
        class_name=(
            f"{class_name} transition-all duration-200 hover:-translate-y-0.5 "
            "hover:shadow-[0_20px_48px_rgba(0,0,0,0.26)]"
            if is_interactive
            else class_name
        ).strip(),
        style=style,
        on_click=on_click,
    )
