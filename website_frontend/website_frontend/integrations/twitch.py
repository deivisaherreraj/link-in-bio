import logging
import os
import time
from typing import Any

import dotenv
import requests

from website_frontend.integrations.observability import log_fail_closed_event
from website_frontend.model.live import Live

REQUEST_TIMEOUT_SECONDS = 5
logger = logging.getLogger(__name__)


class TwitchAPI:
    dotenv.load_dotenv()

    CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")

    def __init__(self) -> None:
        self.token: str | None = None
        self.token_exp: float = 0

    def _log_fail_closed(self, event: str, **context: object) -> None:
        operation = "live" if event == "twitch_live_fetch_failed_closed" else "token"
        log_fail_closed_event(
            logger,
            event=event,
            integration="twitch",
            operation=operation,
            context=context,
        )

    def _offline_live(self, **context: object) -> Live:
        if context:
            self._log_fail_closed("twitch_live_fetch_failed_closed", **context)
        return Live.offline()

    def _normalize_tags(self, raw_value: object) -> list[str]:
        if not isinstance(raw_value, list):
            return []

        normalized: list[str] = []

        for tag in raw_value:
            if not isinstance(tag, str):
                continue

            clean_tag = tag.strip()
            if not clean_tag:
                continue

            normalized.append(clean_tag)

        return normalized

    def generate_token(self) -> None:
        status_code: int | None = None

        try:
            response = requests.post(
                "https://id.twitch.tv/oauth2/token",
                data={
                    "client_id": self.CLIENT_ID,
                    "client_secret": self.CLIENT_SECRET,
                    "grant_type": "client_credentials",
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            status_code = response.status_code

            if response.status_code == 200:
                data: Any = response.json()
                access_token = (
                    data.get("access_token") if isinstance(data, dict) else None
                )
                expires_in = data.get("expires_in") if isinstance(data, dict) else None

                if isinstance(access_token, str) and isinstance(
                    expires_in, int | float
                ):
                    self.token = access_token
                    self.token_exp = time.time() + expires_in
                    return
        except Exception as exc:
            self._log_fail_closed(
                "twitch_token_fetch_failed_closed",
                error_type=type(exc).__name__,
            )
        else:
            self._log_fail_closed(
                "twitch_token_fetch_failed_closed",
                status_code=status_code,
            )

        self.token = None
        self.token_exp = 0

    def token_valid(self) -> bool:
        return time.time() < self.token_exp

    def live(self, user: str) -> Live:
        if not self.token_valid():
            self.generate_token()

        if self.token is None:
            return self._offline_live()

        try:
            response = requests.get(
                "https://api.twitch.tv/helix/streams",
                params={"user_login": user},
                headers={
                    "Client-ID": self.CLIENT_ID,
                    "Authorization": f"Bearer {self.token}",
                },
                timeout=REQUEST_TIMEOUT_SECONDS,
            )

            payload: Any = response.json()
            data = payload.get("data") if isinstance(payload, dict) else None

            if response.status_code == 200 and isinstance(data, list) and data:
                stream = data[0]

                if not isinstance(stream, dict):
                    return self._offline_live(reason="invalid_stream_payload")

                title = stream.get("title")
                category = stream.get("game_name")

                if not isinstance(title, str) or not title.strip():
                    return self._offline_live(reason="missing_title")

                if not isinstance(category, str) or not category.strip():
                    return self._offline_live(reason="missing_category")

                viewer_count = stream.get("viewer_count")
                viewer = viewer_count if isinstance(viewer_count, int) else 0

                return Live.online(
                    title=title.strip(),
                    category=category.strip(),
                    tags=self._normalize_tags(stream.get("tags")),
                    viewer=viewer,
                )
        except Exception as exc:
            return self._offline_live(error_type=type(exc).__name__)

        return self._offline_live(
            status_code=response.status_code,
            reason="offline_or_invalid_payload",
        )
