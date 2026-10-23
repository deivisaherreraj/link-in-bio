from typing import Literal

from pydantic import BaseModel

SocialLinkSection = Literal["work", "community", "resources", "contact"]


class SocialLink(BaseModel):
    label: str
    url: str
    icon: str
    icon_color: str | None = None
    section: SocialLinkSection
    priority: int
    is_active: bool
    is_external: bool
    description: str | None = None
    badge: str | None = None
    badge_color: str | None = None
    border_color: str | None = None
