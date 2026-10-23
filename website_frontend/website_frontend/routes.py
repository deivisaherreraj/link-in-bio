from enum import Enum


# Define las rutas de la aplicación web
class Route(Enum):
    INDEX = "/"
    BLOG = "/blog"
    BLOG_ARTICLE = "/blog/[slug]"
    MAINTENANCE = "/maintenance"
    ERROR_GENERIC = "/error"
    NOT_FOUND = "/[[...splat]]"
