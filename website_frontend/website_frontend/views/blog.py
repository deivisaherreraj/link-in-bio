# ruff: noqa: E501

from __future__ import annotations

import reflex as rx
from reflex.event import EventCallback

from website_frontend.content.blog_articles import (
    BLOG_ARTICLES,
    ArticleSection,
    BlogArticle,
    article_href,
    articles_by_category,
    categories,
)
from website_frontend.routes import Route
from website_frontend.styles.colors import (
    BackgroundColor,
    BorderColor,
    Color,
    TextColor,
)
from website_frontend.styles.fonts import FontSize, FontWeight
from website_frontend.styles.styles import Margin, Padding, Spacing
from website_frontend.views.footer import footer
from website_frontend.views.navbar import navbar


class BlogIndexState(rx.State):
    active_category: str = ""

    @rx.var
    def has_active_category(self) -> bool:
        return self.active_category != ""

    @rx.var
    def filtered_article_count(self) -> int:
        if self.active_category == "":
            return len(BLOG_ARTICLES)

        return len(articles_by_category(self.active_category))

    @rx.event()
    def set_active_category(self, category: str) -> None:
        self.active_category = "" if self.active_category == category else category

    @rx.event
    def clear_active_category(self):
        self.active_category = ""


_set_active_category_event: EventCallback[str] = BlogIndexState.set_active_category


def _page_shell(*children: rx.Component) -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                *children,
                width="100%",
                max_width="980px",
                margin_y=Margin.BIG.value,
                padding=Padding.BIG.value,
                spacing=Spacing.BIG.value,
                align="stretch",
            )
        ),
        footer(),
    )


def _back_link(label: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.el.I.create(class_name="fa-solid fa-arrow-left"),
            rx.text(label),
            align="center",
            spacing=Spacing.SMALL.value,
        ),
        href=href,
        color=Color.PRIMARY.value,
        font_weight=FontWeight.MEDIUM.value,
        width="fit-content",
    )


def _category_badges(article: BlogArticle) -> list[rx.Component]:
    return [
        rx.badge(
            category,
            variant="soft",
            color_scheme="blue",
            radius="full",
            size="2",
        )
        for category in article.categories
    ]


def _meta_row(article: BlogArticle, *, with_note: bool = False) -> rx.Component:
    items = [
        rx.hstack(
            rx.el.I.create(class_name="fa-regular fa-calendar"),
            rx.text(article.published_at),
            align="center",
            spacing=Spacing.VERY_SMALL.value,
        ),
        rx.hstack(
            rx.el.I.create(class_name="fa-regular fa-clock"),
            rx.text(article.read_time),
            align="center",
            spacing=Spacing.VERY_SMALL.value,
        ),
    ]

    if with_note:
        items.append(
            rx.hstack(
                rx.el.I.create(class_name="fa-solid fa-layer-group"),
                rx.text(article.eyebrow),
                align="center",
                spacing=Spacing.VERY_SMALL.value,
            )
        )

    return rx.hstack(
        *items,
        color=TextColor.BODY.value,
        font_size=FontSize.SMALL.value,
        spacing=Spacing.SMALL.value,
        flex_wrap="wrap",
        align="center",
        width="100%",
    )


def _hero_image(article: BlogArticle, *, height: str) -> rx.Component:
    return rx.box(
        rx.image(
            src=article.hero_image,
            alt=article.title,
            width="100%",
            height=height,
            object_fit="cover",
        ),
        overflow="hidden",
        border_radius="24px",
        border=f"1px solid {BorderColor.WHITE_TRANSPARENT.value}",
        width="100%",
        background_color=BackgroundColor.SURFACE.value,
    )


def article_card(article: BlogArticle) -> rx.Component:
    return rx.link(
        rx.vstack(
            _hero_image(article, height="220px"),
            rx.vstack(
                rx.hstack(
                    *_category_badges(article),
                    spacing=Spacing.VERY_SMALL.value,
                    flex_wrap="wrap",
                    width="100%",
                ),
                rx.heading(
                    article.title,
                    as_="h3",
                    font_size=FontSize.LARGE.value,
                    line_height="1.35",
                ),
                rx.text(
                    article.summary,
                    color=TextColor.BODY.value,
                    font_size=FontSize.SMALL.value,
                    line_height="1.7",
                ),
                _meta_row(article),
                spacing=Spacing.SMALL.value,
                align="start",
                width="100%",
            ),
            spacing=Spacing.DEFAULT.value,
            align="start",
            width="100%",
            height="100%",
            padding=Padding.LARGE.value,
            border=f"1px solid {BorderColor.DEFAULT.value}",
            background_color=BackgroundColor.SURFACE.value,
            border_radius="28px",
        ),
        href=article_href(article.slug),
        width="100%",
        height="100%",
    )


def _category_filter_button(category: str) -> rx.Component:
    is_active = BlogIndexState.active_category == category

    return rx.button(
        rx.hstack(
            rx.text(category),
            rx.badge(
                str(len(articles_by_category(category))),
                radius="full",
                variant="soft",
                color_scheme="blue",
            ),
            align="center",
            spacing=Spacing.VERY_SMALL.value,
        ),
        on_click=_set_active_category_event(category),
        width="auto",
        height="auto",
        justify_content="center",
        padding="10px 14px",
        margin_bottom=Margin.ZERO.value,
        border_radius="999px",
        border=rx.cond(
            is_active,
            f"1px solid {Color.PRIMARY.value}",
            f"1px solid {BorderColor.DEFAULT.value}",
        ),
        background_color=rx.cond(
            is_active,
            "rgba(0, 153, 255, 0.18)",
            BackgroundColor.SURFACE.value,
        ),
        color=Color.WHITE.value,
    )


def _all_topics_button() -> rx.Component:
    return rx.button(
        "Todos",
        on_click=BlogIndexState.clear_active_category,
        width="auto",
        height="auto",
        justify_content="center",
        padding="10px 14px",
        margin_bottom=Margin.ZERO.value,
        border_radius="999px",
        border=rx.cond(
            BlogIndexState.has_active_category,
            f"1px solid {BorderColor.DEFAULT.value}",
            f"1px solid {Color.PRIMARY.value}",
        ),
        background_color=rx.cond(
            BlogIndexState.has_active_category,
            BackgroundColor.SURFACE.value,
            "rgba(0, 153, 255, 0.18)",
        ),
        color=Color.WHITE.value,
    )


def _articles_grid_for(articles: tuple[BlogArticle, ...]) -> rx.Component:
    return rx.grid(
        *[article_card(article) for article in articles],
        columns="repeat(auto-fit, minmax(280px, 1fr))",
        spacing=Spacing.DEFAULT.value,
        width="100%",
        align_items="stretch",
    )


def _blog_header() -> rx.Component:
    return rx.vstack(
        rx.heading("Blog", as_="h1", font_size="2.5rem", text_align="center"),
        rx.text(
            "Artículos prácticos sobre backend, frontend, arquitectura y producto.",
            color=TextColor.BODY.value,
            max_width="680px",
            text_align="center",
        ),
        spacing=Spacing.SMALL.value,
        align="center",
        width="100%",
    )


def _category_filter() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Filtrar por categoría",
            color=TextColor.BODY.value,
            font_size=FontSize.SMALL.value,
            text_align="center",
            width="100%",
        ),
        rx.hstack(
            _all_topics_button(),
            *[_category_filter_button(category) for category in categories()],
            spacing=Spacing.SMALL.value,
            flex_wrap="wrap",
            width="100%",
            justify="center",
        ),
        spacing=Spacing.SMALL.value,
        align="center",
        width="100%",
    )


def _empty_state() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("No hay artículos disponibles", as_="h2", font_size="1.75rem"),
            rx.cond(
                BlogIndexState.has_active_category,
                rx.text(
                    "Todavía no hay artículos para la categoría seleccionada.",
                    color=TextColor.BODY.value,
                    text_align="center",
                ),
                rx.text(
                    "Todavía no publiqué artículos en esta sección.",
                    color=TextColor.BODY.value,
                    text_align="center",
                ),
            ),
            spacing=Spacing.SMALL.value,
            align="center",
            width="100%",
        ),
        padding="32px",
        border=f"1px solid {BorderColor.DEFAULT.value}",
        background_color=BackgroundColor.SURFACE.value,
        border_radius="28px",
        width="100%",
    )


def _article_grid() -> rx.Component:
    filtered_results = rx.vstack(
        *[
            rx.cond(
                BlogIndexState.active_category == category,
                _articles_grid_for(articles_by_category(category)),
            )
            for category in categories()
        ],
        width="100%",
    )

    return rx.vstack(
        rx.hstack(
            rx.badge(
                BlogIndexState.filtered_article_count,
                color_scheme="blue",
                variant="soft",
                radius="full",
                size="3",
            ),
            rx.cond(
                BlogIndexState.has_active_category,
                rx.text(
                    "Artículos en la categoría seleccionada.",
                    color=TextColor.BODY.value,
                    font_size=FontSize.SMALL.value,
                ),
                rx.text(
                    "Mostrando todos los artículos.",
                    color=TextColor.BODY.value,
                    font_size=FontSize.SMALL.value,
                ),
            ),
            spacing=Spacing.SMALL.value,
            align="center",
            justify="center",
            flex_wrap="wrap",
            width="100%",
        ),
        rx.cond(
            BlogIndexState.filtered_article_count > 0,
            rx.cond(
                BlogIndexState.has_active_category,
                filtered_results,
                _articles_grid_for(BLOG_ARTICLES),
            ),
            _empty_state(),
        ),
        spacing=Spacing.DEFAULT.value,
        align="stretch",
        width="100%",
    )


def blog_index_view() -> rx.Component:
    return _page_shell(
        _back_link("Volver al inicio", Route.INDEX.value),
        _blog_header(),
        _category_filter(),
        _article_grid(),
    )


def _section_block(section: ArticleSection) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(section.title, as_="h2", font_size="1.75rem"),
            *[
                rx.text(
                    paragraph,
                    color=TextColor.BODY.value,
                    font_size=FontSize.DEFAULT.value,
                    line_height="1.9",
                )
                for paragraph in section.paragraphs
            ],
            *(
                [
                    rx.vstack(
                        *[
                            rx.hstack(
                                rx.el.I.create(class_name="fa-solid fa-angle-right"),
                                rx.text(
                                    item,
                                    color=TextColor.BODY.value,
                                    font_size=FontSize.DEFAULT.value,
                                ),
                                align="start",
                                spacing=Spacing.SMALL.value,
                                width="100%",
                            )
                            for item in section.bullets
                        ],
                        spacing=Spacing.SMALL.value,
                        align="start",
                        width="100%",
                    )
                ]
                if section.bullets
                else []
            ),
            spacing=Spacing.SMALL.value,
            align="start",
            width="100%",
        ),
        width="100%",
    )


def _article_header(article: BlogArticle) -> rx.Component:
    return rx.vstack(
        rx.text(
            article.eyebrow,
            color=Color.PRIMARY.value,
            font_size=FontSize.SMALL.value,
            font_weight=FontWeight.MEDIUM.value,
        ),
        rx.heading(article.title, as_="h1", font_size="2.5rem"),
        rx.text(
            article.summary,
            color=TextColor.BODY.value,
            font_size=FontSize.DEFAULT.value,
            max_width="760px",
        ),
        _meta_row(article, with_note=False),
        rx.hstack(
            *_category_badges(article),
            spacing=Spacing.VERY_SMALL.value,
            flex_wrap="wrap",
            width="100%",
        ),
        spacing=Spacing.SMALL.value,
        align="start",
        width="100%",
    )


def _article_body(article: BlogArticle) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                article.intro,
                color=TextColor.BODY.value,
                font_size=FontSize.DEFAULT.value,
                line_height="1.9",
            ),
            *[_section_block(section) for section in article.sections],
            spacing=Spacing.BIG.value,
            align="start",
            width="100%",
        ),
        width="100%",
    )


def _bottom_navigation() -> rx.Component:
    return rx.box(
        rx.link(
            rx.hstack(
                rx.el.I.create(class_name="fa-solid fa-arrow-left"),
                rx.text("Volver al blog"),
                align="center",
                spacing=Spacing.SMALL.value,
            ),
            href=Route.BLOG.value,
            color=Color.PRIMARY.value,
            font_weight=FontWeight.MEDIUM.value,
        ),
        padding_top=Padding.SMALL.value,
        width="100%",
    )


def blog_article_view(article: BlogArticle) -> rx.Component:
    return _page_shell(
        _back_link("Volver al blog", Route.BLOG.value),
        _article_header(article),
        _hero_image(article, height="360px"),
        _article_body(article),
        _bottom_navigation(),
    )


def blog_article_not_found_view() -> rx.Component:
    return _page_shell(
        _back_link("Volver al blog", Route.BLOG.value),
        rx.box(
            rx.vstack(
                rx.badge(
                    "Slug no disponible",
                    color_scheme="amber",
                    variant="soft",
                    radius="full",
                    size="3",
                ),
                rx.heading("Artículo no encontrado", as_="h1", font_size="2.5rem"),
                rx.text(
                    "Todavía no publiqué ese artículo o el enlace cambió. Mientras tanto, podés volver al índice y seguir leyendo contenido relacionado.",
                    color=TextColor.BODY.value,
                    max_width="680px",
                ),
                rx.grid(
                    *[article_card(article) for article in BLOG_ARTICLES[:3]],
                    columns="repeat(auto-fit, minmax(260px, 1fr))",
                    spacing=Spacing.SMALL.value,
                    width="100%",
                ),
                spacing=Spacing.SMALL.value,
                align="start",
                width="100%",
            ),
            padding="32px",
            border=f"1px solid {BorderColor.DEFAULT.value}",
            background_color=BackgroundColor.SURFACE.value,
            border_radius="32px",
            width="100%",
        ),
    )
