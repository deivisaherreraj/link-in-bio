import os
from urllib.parse import urlparse

import reflex as rx

DEFAULT_API_URL = "http://localhost:8000"


def _normalize_api_url(value: str | None) -> str:
    if value is None:
        return DEFAULT_API_URL

    candidate = value.strip()
    if not candidate:
        return DEFAULT_API_URL

    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return DEFAULT_API_URL

    return candidate


tailwind_plugin = rx.plugins.TailwindV4Plugin(
    {
        "plugins": ["@tailwindcss/typography"],
        "theme": {
            "extend": {
                "colors": {
                    "body": "#05080D",
                    "surface": "#0D1218",
                    "surface-hover": "#161D26",
                    "primary": {
                        "DEFAULT": "#0099FF",
                        "light": "#33ADFF",
                    },
                    "text": {
                        "primary": "#FFFFFF",
                        "secondary": "#94A3B8",
                        "accent": "#38BDF8",
                    },
                    "border": {
                        "subtle": "rgba(255, 255, 255, 0.05)",
                        "highlight": "#0099FF",
                    },
                },
                "fontFamily": {
                    "sans": [
                        "Inter",
                        "-apple-system",
                        "BlinkMacSystemFont",
                        "sans-serif",
                    ],
                },
                "fontSize": {
                    "xs": "0.75rem",
                    "sm": "0.875rem",
                    "base": "1rem",
                    "lg": "1.125rem",
                    "xl": "1.5rem",
                },
                "spacing": {
                    "xs": "4px",
                    "sm": "8px",
                    "md": "16px",
                    "lg": "24px",
                    "xl": "32px",
                    "xxl": "48px",
                },
                "maxWidth": {
                    "container": "680px",
                },
                "borderRadius": {
                    "card": "12px",
                    "full": "9999px",
                },
                "transitionDuration": {
                    "DEFAULT": "200ms",
                },
            }
        },
    }
)

config = rx.Config(
    app_name="website_frontend",  # Nombre de la aplicación Reflex
    api_url=_normalize_api_url(os.getenv("API_URL")),  # URL de la API backend
    plugins=[
        rx.plugins.SitemapPlugin(),  # Habilita la generación automática de sitemaps
        tailwind_plugin,  # Uses Tailwind CSS v4
    ],
    show_built_with_reflex=False,  # Oculta el banner "Built with Reflex"
)
