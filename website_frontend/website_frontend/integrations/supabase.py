import logging
import os
from collections.abc import Mapping

import dotenv
from supabase import Client, create_client

import website_frontend.constants.featured_constants as featured_const
from website_frontend.integrations.observability import log_fail_closed_event
from website_frontend.model.featured import Featured
from website_frontend.model.primary_social import PrimarySocial
from website_frontend.model.profile import Profile
from website_frontend.model.social_link import SocialLink, SocialLinkSection
from website_frontend.shared.urls import (
    is_actionable_external_url,
    is_actionable_href,
    is_actionable_navigation_target,
)

logger = logging.getLogger(__name__)

SOCIAL_LINK_SECTIONS: tuple[SocialLinkSection, ...] = (
    "work",
    "community",
    "resources",
    "contact",
)


class SupabaseAPI:
    dotenv.load_dotenv()

    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

    def __init__(self) -> None:
        if self.SUPABASE_URL is not None and self.SUPABASE_KEY is not None:
            self.supabase: Client = create_client(self.SUPABASE_URL, self.SUPABASE_KEY)

    def _normalize_technologies(self, raw_value: object) -> list[str]:
        """
        Normaliza el campo 'technologies' desde Supabase a List[str].

        Casos posibles:
        - Array/text[] de Supabase -> list
        - Cadena separada por comas -> se hace split
        - None u otro tipo -> []
        """
        if raw_value is None:
            return []

        if isinstance(raw_value, list):
            return self._normalize_string_list(raw_value)

        if isinstance(raw_value, str):
            # Cadena "React, Node.js, MongoDB"
            return [t.strip() for t in raw_value.split(",") if t.strip()]

        # Cualquier otro tipo, se ignora
        return []

    def _normalize_string_list(self, raw_value: object) -> list[str]:
        if not isinstance(raw_value, list):
            return []

        normalized: list[str] = []

        for item in raw_value:
            if not isinstance(item, str):
                continue

            value = item.strip()
            if value:
                normalized.append(value)

        return normalized

    def _get_string(self, payload: Mapping[str, object], key: str) -> str:
        value = payload.get(key)
        if not isinstance(value, str):
            return ""

        return value.strip()

    def _get_optional_string(
        self, payload: Mapping[str, object], key: str
    ) -> str | None:
        value = payload.get(key)
        if not isinstance(value, str):
            return None

        normalized = value.strip()
        return normalized if normalized else None

    def _get_optional_external_url(
        self, payload: Mapping[str, object], key: str
    ) -> str | None:
        value = self._get_optional_string(payload, key)
        if not is_actionable_external_url(value):
            return None

        return value

    def _get_optional_actionable_target(
        self, payload: Mapping[str, object], key: str
    ) -> str | None:
        value = self._get_optional_string(payload, key)
        if value is None or not is_actionable_navigation_target(value):
            return None

        return value

    def _get_optional_email(
        self, payload: Mapping[str, object], key: str
    ) -> str | None:
        value = self._get_optional_string(payload, key)
        if value is None or "@" not in value or " " in value:
            return None

        return value

    def _normalize_social_link_url(
        self, payload: Mapping[str, object], is_external: bool
    ) -> str | None:
        value = self._get_optional_string(payload, "url")
        if value is None:
            return None

        if value in {"/", "#"}:
            return value

        if is_external:
            return value if is_actionable_external_url(value) else "#"

        if is_actionable_navigation_target(value) or value.startswith("mailto:"):
            return value

        return "#" if is_actionable_href(value) else None

    def _normalize_social_links(self, raw_value: object) -> list[SocialLink]:
        if not isinstance(raw_value, list):
            return []

        normalized: list[SocialLink] = []

        for item in raw_value:
            if not isinstance(item, Mapping):
                continue

            payload = dict(item)
            label = self._get_string(payload, "label")
            icon = self._get_string(payload, "icon")
            section = self._get_string(payload, "section").lower()
            is_active = payload.get("is_active")
            is_external = payload.get("is_external")
            priority = payload.get("priority")

            if not label or not icon or section not in SOCIAL_LINK_SECTIONS:
                continue

            if not isinstance(is_active, bool) or not isinstance(is_external, bool):
                continue

            if isinstance(priority, bool) or not isinstance(priority, int):
                continue

            url = self._normalize_social_link_url(payload, is_external)
            if url is None:
                continue

            normalized.append(
                SocialLink(
                    label=label,
                    url=url,
                    icon=icon,
                    section=section,
                    priority=priority,
                    is_active=is_active,
                    is_external=is_external,
                    description=self._get_optional_string(payload, "description"),
                    badge=self._get_optional_string(payload, "badge"),
                    badge_color=self._get_optional_string(payload, "badge_color"),
                    border_color=self._get_optional_string(payload, "border_color"),
                )
            )

        return sorted(normalized, key=lambda item: item.priority)

    def _normalize_primary_socials(self, raw_value: object) -> list[PrimarySocial]:
        if not isinstance(raw_value, list):
            return []

        normalized: list[PrimarySocial] = []

        for item in raw_value:
            if not isinstance(item, Mapping):
                continue

            payload = dict(item)
            label = self._get_string(payload, "label")
            raw_url = self._get_optional_string(payload, "url")
            icon = self._get_string(payload, "icon")
            is_active = payload.get("is_active")
            priority = payload.get("priority")

            if raw_url is None:
                url = None
            elif raw_url.startswith("mailto:"):
                url = raw_url
            else:
                url = self._get_optional_external_url(payload, "url")

            if not label or url is None or not icon:
                continue

            if not isinstance(is_active, bool):
                continue

            if isinstance(priority, bool) or not isinstance(priority, int):
                continue

            normalized.append(
                PrimarySocial(
                    label=label,
                    url=url,
                    icon=icon,
                    is_active=is_active,
                    priority=priority,
                )
            )

        return sorted(normalized, key=lambda item: item.priority)

    def _get_status_config(self, raw_value: object) -> featured_const.ProjectStatus:
        return featured_const.resolve_project_status(raw_value)

    def _normalize_featured_item(
        self, featured_item: Mapping[str, object]
    ) -> Featured | None:
        payload = dict(featured_item)
        title = self._get_string(payload, "title")
        if not title:
            return None

        href = self._get_optional_actionable_target(payload, "href")
        github_url = self._get_optional_external_url(payload, "github_url")
        live_url = self._get_optional_external_url(payload, "live_url")

        if href is None and github_url is None and live_url is None:
            return None

        return Featured(
            href=href,
            image_url=self._get_optional_string(payload, "image_url"),
            title=title,
            description=self._get_optional_string(payload, "description"),
            technologies=self._normalize_technologies(payload.get("technologies")),
            github_url=github_url,
            live_url=live_url,
            status=self._get_status_config(payload.get("status")),
        )

    def featured(self) -> list[Featured]:
        if not hasattr(self, "supabase"):
            return []

        try:
            response = (
                self.supabase.table("featured")
                .select("*")
                .order("init_date", desc=True)
                .limit(4)
                .execute()
            )

            featured_data: list[Featured] = []

            if len(response.data) > 0:
                for featured_item in response.data:
                    if not isinstance(featured_item, Mapping):
                        continue

                    normalized_item = self._normalize_featured_item(featured_item)
                    if normalized_item is None:
                        continue

                    featured_data.append(normalized_item)

            return featured_data
        except Exception as exc:
            log_fail_closed_event(
                logger,
                event="supabase_featured_fetch_failed_closed",
                integration="supabase",
                operation="featured",
                context={"error_type": type(exc).__name__},
            )
            return []

    def profile(self, fallback: Profile | None = None) -> Profile | None:
        if not hasattr(self, "supabase"):
            return None

        try:
            response = self.supabase.table("profile").select("*").limit(1).execute()

            if not isinstance(response.data, list) or len(response.data) == 0:
                return None

            profile_row = response.data[0]
            if not isinstance(profile_row, Mapping):
                return None

            payload = dict(profile_row)
            full_name = self._get_string(payload, "full_name")
            handle = self._get_string(payload, "handle")
            headline = self._get_string(payload, "headline")
            bio_short = self._get_string(payload, "bio_short")
            avatar_url = self._get_optional_actionable_target(payload, "avatar_url")
            email = self._get_optional_email(payload, "email")
            availability_status_key = self._get_string(
                payload, "availability_status_key"
            )
            tech_stack_summary = self._get_string(payload, "tech_stack_summary")
            bio_short_highlights = self._normalize_string_list(
                payload.get("bio_short_highlights")
            )
            primary_socials = self._normalize_primary_socials(
                payload.get("primary_socials")
            )

            if fallback is not None:
                full_name = full_name or fallback.full_name
                handle = handle or fallback.handle
                headline = headline or fallback.headline
                bio_short = bio_short or fallback.bio_short
                avatar_url = avatar_url or fallback.avatar_url
                email = email or fallback.email
                availability_status_key = (
                    availability_status_key or fallback.availability_status_key
                )
                tech_stack_summary = tech_stack_summary or fallback.tech_stack_summary

                if not bio_short_highlights and bio_short == fallback.bio_short:
                    bio_short_highlights = list(fallback.bio_short_highlights)

                if not primary_socials:
                    primary_socials = list(fallback.primary_socials)

            if not all(
                [
                    full_name,
                    handle,
                    headline,
                    bio_short,
                    avatar_url,
                    email,
                    availability_status_key,
                    tech_stack_summary,
                ]
            ):
                return None

            if avatar_url is None or email is None:
                return None

            return Profile(
                full_name=full_name,
                handle=handle,
                headline=headline,
                bio_short=bio_short,
                bio_short_highlights=bio_short_highlights,
                avatar_url=avatar_url,
                email=email,
                availability_status_key=availability_status_key,
                tech_stack_summary=tech_stack_summary,
                primary_socials=primary_socials,
            )
        except Exception as exc:
            log_fail_closed_event(
                logger,
                event="supabase_profile_fetch_failed_closed",
                integration="supabase",
                operation="profile",
                context={"error_type": type(exc).__name__},
            )
            return None

    def social_links(self) -> list[SocialLink]:
        if not hasattr(self, "supabase"):
            return []

        try:
            response = self.supabase.table("social_links").select("*").execute()

            if not isinstance(response.data, list) or len(response.data) == 0:
                return []

            return self._normalize_social_links(response.data)
        except Exception as exc:
            log_fail_closed_event(
                logger,
                event="supabase_social_links_fetch_failed_closed",
                integration="supabase",
                operation="social_links",
                context={"error_type": type(exc).__name__},
            )
            return []
