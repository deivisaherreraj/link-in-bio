from urllib.parse import urlparse


def is_actionable_href(url: str | None) -> bool:
    if url is None:
        return False

    candidate = url.strip()
    return bool(candidate) and candidate not in {"/", "#"}


def is_actionable_external_url(url: str | None) -> bool:
    if url is None or not is_actionable_href(url):
        return False

    parsed = urlparse(url.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_actionable_internal_route(url: str | None) -> bool:
    if url is None or not is_actionable_href(url):
        return False

    candidate = url.strip()
    parsed = urlparse(candidate)
    return not parsed.scheme and not parsed.netloc and candidate.startswith("/")


def is_actionable_navigation_target(url: str | None) -> bool:
    return is_actionable_external_url(url) or is_actionable_internal_route(url)
