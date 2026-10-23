from reflex.istate.data import RouterData

from website_frontend.content.blog_articles import BLOG_ARTICLES
from website_frontend.pages.blog import blog
from website_frontend.pages.blog_article import BlogArticleState, blog_article
from website_frontend.views.blog import blog_article_not_found_view, blog_article_view


def test_blog_page_renders_reference_aligned_index() -> None:
    rendered = str(blog())

    assert "Volver al inicio" in rendered
    assert (
        "Art\\u00edculos pr\\u00e1cticos sobre backend, frontend, "
        "arquitectura y producto." in rendered
    )
    assert "Filtrar por categor\\u00eda" in rendered
    assert (
        "C\\u00f3mo estructurar una API .NET para un SaaS sin perder mantenibilidad"
        in rendered
    )
    assert "/blog/estructurar-api-net-saas" in rendered
    assert "Mostrando todos los art\\u00edculos." in rendered
    assert "set_active_category" in rendered
    assert "clear_active_category" in rendered


def test_blog_article_view_renders_reference_aligned_article() -> None:
    rendered = str(blog_article_view(BLOG_ARTICLES[0]))

    assert "Clean architecture aplicada" in rendered
    assert "Volver al blog" in rendered
    assert (
        "C\\u00f3mo estructurar una API .NET para un SaaS sin perder mantenibilidad"
        in rendered
    )
    assert "12 Nov 2025" in rendered
    assert (
        "El dominio no deber\\u00eda conocer frameworks, HTTP ni bases de datos."
        not in rendered
    )
    assert "Angular Signals y fronteras de UI" not in rendered


def test_blog_article_page_uses_slug_matching_and_fallback() -> None:
    rendered = str(blog_article())
    fallback = str(blog_article_not_found_view())

    assert "switch (JSON.stringify" in rendered
    assert "slug_rx_state" in rendered
    assert "Art\\u00edculo no encontrado" in fallback
    assert "/blog/reflex-product-pages-contenido-estatico" in fallback


def test_blog_article_state_reads_slug_from_router_url() -> None:
    cases: tuple[tuple[str, dict[str, str], str], ...] = (
        ("/blog/example", {"slug": "example"}, "example"),
        ("/blog/caf%C3%A9/?preview=true", {"slug": "café"}, "café"),
        ("/blog/", {}, ""),
    )

    for path, query, expected in cases:
        router = RouterData.from_router_data(
            {
                "pathname": "/blog/[slug]",
                "asPath": path,
                "query": query,
                "headers": {"origin": "http://localhost:3000"},
            }
        )
        state = object.__new__(BlogArticleState)
        object.__setattr__(state, "router", router)

        assert state.article_slug == expected
