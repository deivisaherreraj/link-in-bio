from website_frontend.constants.site_constants import EMAIL
from website_frontend.integrations.supabase import SupabaseAPI
from website_frontend.model.social_link import SocialLink, SocialLinkSection
from website_frontend.styles.styles import Color

SUPABASE_API = SupabaseAPI()

SOCIAL_LINK_SECTION_ORDER: tuple[SocialLinkSection, ...] = (
    "work",
    "community",
    "resources",
    "contact",
)


def _default_icon_color(link: SocialLink) -> str | None:
    normalized_label = link.label.strip().lower()

    if "discord" in normalized_label:
        return Color.DISCORD.value

    if "youtube" in normalized_label:
        return Color.RED.value

    if "twitch" in normalized_label:
        return Color.PURPLE.value

    return None


def _normalize_link_presentation(link: SocialLink) -> SocialLink:
    return link.model_copy(
        update={
            "badge": link.badge
            if link.badge is not None
            else ("Próximamente" if not link.is_active else None),
            "icon_color": link.icon_color or _default_icon_color(link),
        }
    )


def get_default_social_links() -> list[SocialLink]:
    return [
        SocialLink(
            label="Email",
            url=f"mailto:{EMAIL}",
            icon="fa-solid fa-envelope",
            section="contact",
            priority=1,
            is_active=True,
            is_external=False,
            description="Envíame un correo electrónico para consultas directas.",
            badge="Correo",
            badge_color=Color.GRAY_DARK.value,
        ),
    ]


def get_social_links() -> list[SocialLink]:
    social_links = [
        _normalize_link_presentation(link) for link in SUPABASE_API.social_links()
    ]
    if social_links:
        return social_links

    return [_normalize_link_presentation(link) for link in get_default_social_links()]


def get_social_links_by_section() -> dict[SocialLinkSection, list[SocialLink]]:
    grouped: dict[SocialLinkSection, list[SocialLink]] = {
        section: [] for section in SOCIAL_LINK_SECTION_ORDER
    }

    for link in get_social_links():
        grouped[link.section].append(link)

    return grouped
