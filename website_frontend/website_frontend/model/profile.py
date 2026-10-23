from pydantic import BaseModel, Field, model_validator

from website_frontend.model.primary_social import PrimarySocial


def _normalize_highlights(highlights: list[str]) -> list[str]:
    normalized: list[str] = []

    for highlight in highlights:
        if not isinstance(highlight, str):
            continue

        value = highlight.strip()
        if value and value not in normalized:
            normalized.append(value)

    return normalized


class ProfileBioSegment(BaseModel):
    text: str
    is_highlighted: bool = False


def _build_bio_segments(
    bio_short: str, highlights: list[str]
) -> list[ProfileBioSegment]:
    if not bio_short:
        return []

    if not highlights:
        return [ProfileBioSegment(text=bio_short)]

    segments: list[ProfileBioSegment] = []
    cursor = 0

    while cursor < len(bio_short):
        matches = [
            (start_index, highlight)
            for highlight in highlights
            for start_index in [bio_short.find(highlight, cursor)]
            if start_index >= 0
        ]

        if not matches:
            segments.append(ProfileBioSegment(text=bio_short[cursor:]))
            break

        start_index, highlight = min(matches, key=lambda item: (item[0], -len(item[1])))

        if start_index > cursor:
            segments.append(ProfileBioSegment(text=bio_short[cursor:start_index]))

        segments.append(ProfileBioSegment(text=highlight, is_highlighted=True))
        cursor = start_index + len(highlight)

    return segments


class Profile(BaseModel):
    full_name: str
    handle: str
    headline: str
    bio_short: str
    bio_short_highlights: list[str] = Field(default_factory=list)
    bio_short_segments: list[ProfileBioSegment] = Field(default_factory=list)
    avatar_url: str
    email: str
    availability_status_key: str
    tech_stack_summary: str
    primary_socials: list[PrimarySocial] = Field(default_factory=list)

    @model_validator(mode="after")
    def sync_bio_short_segments(self):
        self.bio_short_highlights = _normalize_highlights(self.bio_short_highlights)
        self.bio_short_segments = _build_bio_segments(
            self.bio_short,
            self.bio_short_highlights,
        )
        return self
