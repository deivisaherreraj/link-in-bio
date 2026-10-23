from urllib.parse import unquote

import reflex as rx

import website_frontend.shared.browser as browser
import website_frontend.shared.meta as meta
from website_frontend.content.blog_articles import BLOG_ARTICLES
from website_frontend.routes import Route
from website_frontend.views.blog import blog_article_not_found_view, blog_article_view


class BlogArticleState(rx.State):
    @rx.var
    def article_slug(self) -> str:
        path = self.router.url.path.rstrip("/")
        prefix = f"{Route.BLOG.value}/"
        if not path.startswith(prefix):
            return ""

        slug = unquote(path.removeprefix(prefix))
        return slug if "/" not in slug else ""


@rx.page(
    route=Route.BLOG_ARTICLE.value,
    title=meta.blog_article_title,
    description=meta.blog_article_description,
    image=meta.preview,
    meta=meta.blog_article_meta,
)
def blog_article() -> rx.Component:
    cases = [(article.slug, blog_article_view(article)) for article in BLOG_ARTICLES]

    return rx.box(
        browser.lang(),
        rx.match(
            BlogArticleState.article_slug,
            *cases,
            blog_article_not_found_view(),
        ),
    )
