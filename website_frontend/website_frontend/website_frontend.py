import reflex as rx

import website_frontend.constants.site_constants as const
import website_frontend.pages.blog  # noqa: F401
import website_frontend.pages.blog_article  # noqa: F401
import website_frontend.pages.error  # noqa: F401
import website_frontend.pages.index  # noqa: F401
import website_frontend.pages.maintenance  # noqa: F401
import website_frontend.pages.not_found  # noqa: F401
import website_frontend.styles.styles as styles

# Importa la aplicación FastAPI desde el módulo api
from website_frontend.api.api import fastapi_app
from website_frontend.integrations.observability import configure_application_logging

configure_application_logging()

# Google tag (gtag.js)
app = rx.App(
    stylesheets=styles.STYLESHEETS,
    style=styles.BASE_STYLE,
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
        gray_color="slate",
        radius="medium",
        scaling="100%",
        has_background=False,
        panel_background="translucent",
    ),
    head_components=[
        rx.script(src=f"https://www.googletagmanager.com/gtag/js?id={const.G_TAG}"),
        rx.script(
            f"""
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{const.G_TAG}');
            """
        ),
    ],
    api_transformer=fastapi_app,
)
