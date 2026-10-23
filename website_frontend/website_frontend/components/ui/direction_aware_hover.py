from operator import ne

import reflex as rx

from website_frontend.styles.styles import Color, Padding

DEFAULT_FEATURED_IMAGE = "/featured-default.svg"


def direction_aware_hover(
    image_url: str | None,
    children: rx.Component,
) -> rx.Component:
    resolved_image_url = rx.cond(ne(image_url, None), image_url, DEFAULT_FEATURED_IMAGE)

    return rx.card(
        rx.box(
            rx.image(
                src=resolved_image_url,
                alt="",
                position="absolute",
                inset="0",
                width="100%",
                height="100%",
                object_fit="cover",
                z_index="0",
                class_name="featured-image",
            ),
            rx.box(
                position="absolute",
                inset="0",
                width="100%",
                height="100%",
                z_index="5",
                background=(
                    "linear-gradient(180deg, rgba(4, 8, 15, 0.05) 0%, "
                    "rgba(4, 8, 15, 0.22) 58%, rgba(4, 8, 15, 0.65) 100%)"
                ),
            ),
            rx.box(
                position="absolute",
                inset="0",
                width="100%",
                height="100%",
                z_index="10",
                bg_color=Color.BG_BLACK_TRANSPARENT_STRONG.value,
                class_name="featured-scrim",
            ),
            rx.flex(
                rx.box(
                    children,
                    position="relative",
                    z_index="20",
                    width="100%",
                ),
                position="absolute",
                inset="0",
                align_items="stretch",
                justify_content="flex-end",
                padding_y=Padding.DEFAULT.value,
                padding_x=Padding.DEFAULT.value,
                z_index="20",
                class_name="featured-overlay",
            ),
            position="relative",
            height="100%",
            width="100%",
            background=(
                "linear-gradient(135deg, rgba(99, 102, 241, 0.28) 0%, "
                "rgba(15, 23, 42, 0.92) 100%)"
            ),
        ),
        position="relative",
        overflow="hidden",
        width="100%",
        height="288px",
        border_color=Color.TRANSPARENT.value,
        padding=Padding.ZERO.value,
        cursor="pointer",
        background=Color.TRANSPARENT.value,
        class_name="featured-hover-card",
    )
