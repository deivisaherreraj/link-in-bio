import reflex as rx

from website_frontend.styles.colors import (
    BackgroundColor,
    BorderColor,
    Color,
    TextColor,
)
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Margin, Padding, Radius, Size, Spacing
from website_frontend.views.footer import footer
from website_frontend.views.navbar import navbar


def _page_shell(content: rx.Component) -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(content),
        footer(),
    )


def _action(
    label: str,
    href: str,
    *,
    is_primary: bool = True,
    accent: str = Color.PRIMARY.value,
    icon: str | None = None,
) -> rx.Component:
    return rx.link(
        rx.button(
            rx.hstack(
                *(
                    [
                        rx.el.I.create(
                            class_name=icon,
                            font_size=FontSize.SMALL.value,
                        )
                    ]
                    if icon
                    else []
                ),
                rx.text(label),
                spacing=Spacing.VERY_SMALL.value,
                align="center",
            ),
            width="auto",
            justify_content="center",
            align_items="center",
            padding_x=Padding.BIG.value,
            background_color=(accent if is_primary else BackgroundColor.SURFACE.value),
            border=(
                f"1px solid {accent}"
                if is_primary
                else f"1px solid {BorderColor.WHITE_TRANSPARENT.value}"
            ),
            color=Color.WHITE.value,
        ),
        href=href,
    )


def _detail_card(
    title: str,
    description: str | None,
    icon: str,
    accent: str,
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.el.I.create(class_name=icon),
                width="40px",
                height="40px",
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius=Radius.FULL.value,
                background_color=BackgroundColor.LIGHT.value,
                color=accent,
                font_size=FontSize.DEFAULT.value,
                border=f"1px solid {BorderColor.WHITE_TRANSPARENT_LIGHT.value}",
            ),
            rx.vstack(
                rx.text(
                    title,
                    size="3",
                    color=Color.WHITE.value,
                    font_weight=FontWeight.MEDIUM.value,
                ),
                *(
                    [
                        rx.text(
                            description,
                            color=TextColor.BODY.value,
                            font_size=FontSize.SMALL.value,
                        )
                    ]
                    if description
                    else []
                ),
                align="start",
                spacing=Spacing.VERY_SMALL.value,
                width="100%",
            ),
            align="center",
            width="100%",
            spacing=Spacing.SMALL.value,
        ),
        padding=Padding.LARGE.value,
        border=f"1px solid {BorderColor.DEFAULT.value}",
        background_color=BackgroundColor.SURFACE.value,
        border_radius="20px",
        width="100%",
    )


def _status_chip(label: str, *, color_scheme: str) -> rx.Component:
    return rx.badge(
        label,
        color_scheme=color_scheme,
        variant="soft",
        radius="full",
        size="3",
    )


def _icon_hero(icon: str, *, accent: str, gradient: str, shadow: str) -> rx.Component:
    return rx.box(
        rx.el.I.create(class_name=icon),
        font_size="40px",
        color=accent,
        width="88px",
        height="88px",
        display="flex",
        align_items="center",
        justify_content="center",
        border_radius=Radius.FULL.value,
        background=gradient,
        border=f"1px solid {BorderColor.WHITE_TRANSPARENT.value}",
        box_shadow=shadow,
    )


def _panel(*children: rx.Component, background: str | None = None) -> rx.Component:
    return rx.box(
        rx.vstack(
            *children,
            spacing=Spacing.SMALL.value,
            align="start",
            width="100%",
        ),
        width="100%",
        padding=Padding.BIG.value,
        border=f"1px solid {BorderColor.DEFAULT.value}",
        background=(
            background
            or "linear-gradient(180deg, rgba(13, 18, 24, 0.98), rgba(12, 21, 29, 0.94))"
        ),
        border_radius="28px",
    )


def _info_panel(*, eyebrow: str, title: str, body: str, accent: str) -> rx.Component:
    return _panel(
        rx.vstack(
            rx.text(
                eyebrow,
                size="3",
                color=accent,
                font_weight=FontWeight.SEMI_BOLD.value,
            ),
            rx.text(
                title,
                size="4",
                color=Color.WHITE.value,
                font_weight=FontWeight.MEDIUM.value,
            ),
            rx.text(
                body,
                color=TextColor.BODY.value,
                font_size=FontSize.SMALL.value,
            ),
            align="start",
            spacing=Spacing.VERY_SMALL.value,
            width="100%",
        )
    )


def _maintenance_checklist_icon(title: str) -> str:
    normalized_title = title.strip().lower()

    if "blog" in normalized_title:
        return "fa-solid fa-newspaper"

    if "esperar" in normalized_title or "publicaci" in normalized_title:
        return "fa-regular fa-clock"

    return "fa-solid fa-calendar-days"


def system_page(
    *,
    status_label: str,
    title: str,
    message: str,
    icon: str,
    primary_label: str,
    primary_href: str,
    secondary_label: str,
    secondary_href: str,
    detail_title: str,
    detail_body: str,
    checklist_title: str,
    checklist_items: list[str],
    note: str,
) -> rx.Component:
    return _page_shell(
        rx.vstack(
            _status_chip(status_label, color_scheme="blue"),
            _icon_hero(
                icon,
                accent=Color.PRIMARY.value,
                gradient=(
                    "linear-gradient(180deg, rgba(0, 153, 255, 0.18), "
                    "rgba(12, 21, 29, 0.95))"
                ),
                shadow="0 18px 40px rgba(0, 153, 255, 0.18)",
            ),
            rx.vstack(
                rx.heading(
                    title,
                    as_="h1",
                    font_size="2.5rem",
                    text_align="center",
                ),
                rx.text(
                    message,
                    color=TextColor.BODY.value,
                    font_size=FontSize.DEFAULT.value,
                    text_align="center",
                    max_width="620px",
                ),
                spacing=Spacing.SMALL.value,
                align="center",
                width="100%",
            ),
            rx.hstack(
                _action(primary_label, primary_href, is_primary=True),
                _action(secondary_label, secondary_href, is_primary=False),
                spacing=Spacing.SMALL.value,
                justify="center",
                flex_wrap="wrap",
                width="100%",
            ),
            _panel(
                rx.text(
                    detail_title,
                    size="4",
                    color=Color.WHITE.value,
                    font_weight=FontWeight.MEDIUM.value,
                ),
                rx.text(
                    detail_body,
                    color=TextColor.BODY.value,
                    font_size=FontSize.SMALL.value,
                ),
                rx.divider(margin_y=Margin.SMALL.value),
                rx.text(
                    checklist_title,
                    size="3",
                    color=Color.PRIMARY.value,
                    font_weight=FontWeight.MEDIUM.value,
                ),
                rx.vstack(
                    *[
                        _detail_card(
                            title=item,
                            description="",
                            icon="fa-solid fa-check",
                            accent=Color.PRIMARY.value,
                        )
                        for item in checklist_items
                    ],
                    spacing=Spacing.SMALL.value,
                    width="100%",
                ),
            ),
            rx.text(
                note,
                color=TextColor.BODY.value,
                font_size=FontSize.SMALL.value,
                text_align="center",
                max_width="620px",
            ),
            width="100%",
            max_width="760px",
            min_height="calc(100vh - 220px)",
            justify="center",
            align="center",
            spacing=Spacing.BIG.value,
            padding=Size.BIG.value,
            margin_y=Margin.BIG.value,
        )
    )


def maintenance_page(
    *,
    status_label: str,
    title: str,
    message: str,
    eta_title: str,
    eta_value: str,
    eta_message: str,
    primary_label: str,
    primary_href: str,
    secondary_label: str,
    secondary_href: str,
    checklist_title: str,
    checklist_items: list[str],
    note: str,
) -> rx.Component:
    accent = Color.ORANGE.value

    return _page_shell(
        rx.vstack(
            rx.hstack(
                _status_chip(status_label, color_scheme="orange"),
                _status_chip("Maintenance active", color_scheme="orange"),
                spacing=Spacing.VERY_SMALL.value,
                justify="center",
                flex_wrap="wrap",
                width="100%",
            ),
            _icon_hero(
                "fa-solid fa-screwdriver-wrench",
                accent=accent,
                gradient=(
                    "linear-gradient(180deg, rgba(245, 158, 11, 0.24), "
                    "rgba(29, 19, 10, 0.95))"
                ),
                shadow="0 18px 40px rgba(245, 158, 11, 0.22)",
            ),
            rx.vstack(
                rx.heading(
                    title,
                    as_="h1",
                    font_size="2.5rem",
                    text_align="center",
                ),
                rx.text(
                    message,
                    color=TextColor.BODY.value,
                    font_size=FontSize.DEFAULT.value,
                    text_align="center",
                    max_width="640px",
                ),
                spacing=Spacing.SMALL.value,
                align="center",
                width="100%",
            ),
            rx.hstack(
                _action(
                    primary_label,
                    primary_href,
                    is_primary=True,
                    accent=accent,
                    icon="fa-solid fa-rotate-right",
                ),
                _action(secondary_label, secondary_href, is_primary=False),
                spacing=Spacing.SMALL.value,
                justify="center",
                flex_wrap="wrap",
                width="100%",
            ),
            rx.grid(
                _info_panel(
                    eyebrow="Estado del mantenimiento",
                    title="Trabajando ahora mismo",
                    body=(
                        "Estoy publicando mejoras visuales y dejando estable cada "
                        "ajuste antes de reabrir el sitio completo."
                    ),
                    accent=accent,
                ),
                _info_panel(
                    eyebrow=eta_title,
                    title=eta_value,
                    body=eta_message,
                    accent=accent,
                ),
                _info_panel(
                    eyebrow="Validación final",
                    title="Publicación cuidada",
                    body=(
                        "Estoy revisando alineación, interacciones y consistencia "
                        "visual antes de volver a abrir la experiencia completa."
                    ),
                    accent=accent,
                ),
                columns=rx.breakpoints(initial="1", md="3"),
                spacing=Spacing.SMALL.value,
                width="100%",
            ),
            _panel(
                rx.text(
                    checklist_title,
                    size="4",
                    color=Color.WHITE.value,
                    font_weight=FontWeight.MEDIUM.value,
                ),
                rx.vstack(
                    *[
                        _detail_card(
                            title=item,
                            description="",
                            icon=_maintenance_checklist_icon(item),
                            accent=accent,
                        )
                        for item in checklist_items
                    ],
                    spacing=Spacing.SMALL.value,
                    width="100%",
                ),
            ),
            rx.text(
                note,
                color=TextColor.BODY.value,
                font_size=FontSize.SMALL.value,
                text_align="center",
                max_width="640px",
            ),
            width="100%",
            max_width="820px",
            min_height="calc(100vh - 220px)",
            justify="center",
            align="center",
            spacing=Spacing.BIG.value,
            padding=Size.BIG.value,
            margin_y=Margin.BIG.value,
        )
    )


def error_page(
    *,
    status_label: str,
    title: str,
    message: str,
    primary_label: str,
    primary_href: str,
    secondary_label: str,
    secondary_href: str,
    recovery_title: str,
    recovery_body: str,
    note: str,
) -> rx.Component:
    accent = Color.RED.value

    return _page_shell(
        rx.vstack(
            _status_chip(status_label, color_scheme="red"),
            _icon_hero(
                "fa-solid fa-triangle-exclamation",
                accent=accent,
                gradient=(
                    "linear-gradient(180deg, rgba(255, 0, 0, 0.22), "
                    "rgba(29, 10, 10, 0.95))"
                ),
                shadow="0 18px 40px rgba(255, 0, 0, 0.18)",
            ),
            rx.vstack(
                rx.heading(
                    title,
                    as_="h1",
                    font_size="2.5rem",
                    text_align="center",
                ),
                rx.text(
                    message,
                    color=TextColor.BODY.value,
                    font_size=FontSize.DEFAULT.value,
                    text_align="center",
                    max_width="620px",
                ),
                spacing=Spacing.SMALL.value,
                align="center",
                width="100%",
            ),
            rx.hstack(
                _action(
                    primary_label,
                    primary_href,
                    is_primary=True,
                    accent=accent,
                    icon="fa-solid fa-rotate-right",
                ),
                _action(
                    secondary_label,
                    secondary_href,
                    is_primary=False,
                    icon="fa-solid fa-house",
                ),
                spacing=Spacing.SMALL.value,
                justify="center",
                flex_wrap="wrap",
                width="100%",
            ),
            _panel(
                rx.hstack(
                    rx.box(
                        rx.el.I.create(class_name="fa-solid fa-circle-exclamation"),
                        width="40px",
                        height="40px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        border_radius=Radius.FULL.value,
                        background_color="rgba(255, 0, 0, 0.12)",
                        color=accent,
                        border="1px solid rgba(255, 0, 0, 0.2)",
                    ),
                    rx.vstack(
                        rx.text(
                            recovery_title,
                            size="4",
                            color=Color.WHITE.value,
                            font_weight=FontWeight.MEDIUM.value,
                        ),
                        rx.text(
                            recovery_body,
                            color=TextColor.BODY.value,
                            font_size=FontSize.SMALL.value,
                        ),
                        align="start",
                        spacing=Spacing.VERY_SMALL.value,
                        width="100%",
                    ),
                    spacing=Spacing.SMALL.value,
                    align="center",
                    width="100%",
                ),
                rx.divider(margin_y=Margin.SMALL.value),
                rx.grid(
                    _detail_card(
                        title="Intentar de nuevo",
                        description=(
                            "Recargá esta vista para comprobar si el fallo fue "
                            "temporal."
                        ),
                        icon="fa-solid fa-rotate-right",
                        accent=accent,
                    ),
                    _detail_card(
                        title="Volver al inicio",
                        description=(
                            "Usá la portada para recuperar navegación estable de "
                            "inmediato."
                        ),
                        icon="fa-solid fa-house",
                        accent=accent,
                    ),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing=Spacing.SMALL.value,
                    width="100%",
                ),
                rx.text(
                    "Si necesitás una ruta alternativa, el blog suele seguir "
                    "disponible mientras termino de corregir el problema.",
                    color=TextColor.BODY.value,
                    font_size=FontSize.SMALL.value,
                ),
            ),
            rx.text(
                note,
                color=TextColor.BODY.value,
                font_size=FontSize.SMALL.value,
                text_align="center",
                max_width="620px",
            ),
            width="100%",
            max_width="760px",
            min_height="calc(100vh - 220px)",
            justify="center",
            align="center",
            spacing=Spacing.BIG.value,
            padding=Size.BIG.value,
            margin_y=Margin.BIG.value,
        )
    )
