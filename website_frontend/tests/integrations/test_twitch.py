from typing import Any

from website_frontend.integrations import twitch


class StubResponse:
    def __init__(self, status_code: int, payload: dict[str, Any]) -> None:
        self.status_code = status_code
        self.payload = payload

    def json(self) -> dict[str, Any]:
        return self.payload


def test_generate_token_saves_token_and_expiration(monkeypatch):
    api = twitch.TwitchAPI()
    calls: list[tuple[str, dict[str, str], int]] = []

    def fake_post(url, data, timeout):
        calls.append((url, data, timeout))
        return StubResponse(
            200,
            {"access_token": "token-123", "expires_in": 3600},
        )

    monkeypatch.setattr(twitch.time, "time", lambda: 100)
    monkeypatch.setattr(
        twitch.requests,
        "post",
        fake_post,
    )

    api.generate_token()

    assert api.token == "token-123"
    assert api.token_exp == 3700
    assert calls == [
        (
            "https://id.twitch.tv/oauth2/token",
            {
                "client_id": api.CLIENT_ID,
                "client_secret": api.CLIENT_SECRET,
                "grant_type": "client_credentials",
            },
            twitch.REQUEST_TIMEOUT_SECONDS,
        )
    ]


def test_generate_token_clears_state_on_failure(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "old-token"
    api.token_exp = 999

    monkeypatch.setattr(
        twitch.requests,
        "post",
        lambda url, data, timeout: StubResponse(500, {}),
    )

    api.generate_token()

    assert api.token is None
    assert api.token_exp == 0


def test_generate_token_logs_fail_closed_warning(monkeypatch, caplog):
    api = twitch.TwitchAPI()

    monkeypatch.setattr(
        twitch.requests,
        "post",
        lambda url, data, timeout: StubResponse(500, {}),
    )

    with caplog.at_level("WARNING"):
        api.generate_token()

    assert caplog.records[-1].message == "twitch_token_fetch_failed_closed"
    assert caplog.records[-1].event == "twitch_token_fetch_failed_closed"
    assert caplog.records[-1].integration == "twitch"
    assert caplog.records[-1].operation == "token"
    assert caplog.records[-1].fail_closed is True
    assert caplog.records[-1].status_code == 500


def test_generate_token_clears_state_on_request_failure(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "old-token"
    api.token_exp = 999

    def fake_post(url, data, timeout):
        raise twitch.requests.RequestException("network down")

    monkeypatch.setattr(twitch.requests, "post", fake_post)

    api.generate_token()

    assert api.token is None
    assert api.token_exp == 0


def test_generate_token_fails_closed_on_json_failure(monkeypatch, caplog):
    api = twitch.TwitchAPI()
    api.token = "old-token"
    api.token_exp = 999

    class BrokenJsonResponse(StubResponse):
        def json(self) -> dict[str, Any]:
            raise ValueError("sensitive response details")

    monkeypatch.setattr(
        twitch.requests,
        "post",
        lambda url, data, timeout: BrokenJsonResponse(200, {}),
    )

    with caplog.at_level("WARNING"):
        api.generate_token()

    assert api.token is None
    assert api.token_exp == 0
    assert caplog.records[-1].message == "twitch_token_fetch_failed_closed"
    assert caplog.records[-1].event == "twitch_token_fetch_failed_closed"
    assert caplog.records[-1].integration == "twitch"
    assert caplog.records[-1].operation == "token"
    assert caplog.records[-1].fail_closed is True
    assert caplog.records[-1].error_type == "ValueError"
    assert "sensitive response details" not in caplog.text


def test_token_valid_depends_on_current_time(monkeypatch):
    api = twitch.TwitchAPI()
    api.token_exp = 150

    monkeypatch.setattr(twitch.time, "time", lambda: 100)
    assert api.token_valid() is True

    monkeypatch.setattr(twitch.time, "time", lambda: 200)
    assert api.token_valid() is False


def test_live_returns_offline_when_token_json_is_malformed(monkeypatch):
    api = twitch.TwitchAPI()
    get_calls = []

    class BrokenJsonResponse(StubResponse):
        def json(self) -> dict[str, Any]:
            raise ValueError("bad json")

    monkeypatch.setattr(
        twitch.requests,
        "post",
        lambda url, data, timeout: BrokenJsonResponse(200, {}),
    )
    monkeypatch.setattr(
        twitch.requests,
        "get",
        lambda url, params, headers, timeout: get_calls.append(True),
    )

    result = api.live("dherrerajdev")

    assert result == api._offline_live()
    assert api.token is None
    assert api.token_exp == 0
    assert get_calls == []


def test_live_generates_token_and_maps_online_payload(monkeypatch):
    api = twitch.TwitchAPI()
    generated = []
    calls: list[tuple[str, dict[str, str], dict[str, str], int]] = []

    def fake_generate_token():
        generated.append(True)
        api.token = "fresh-token"
        api.token_exp = 999

    def fake_get(url, params, headers, timeout):
        calls.append((url, params, headers, timeout))
        return StubResponse(
            200,
            {
                "data": [
                    {
                        "title": "Live coding",
                        "game_name": "Software and Game Development",
                        "tags": ["python", "reflex"],
                        "viewer_count": 42,
                    }
                ]
            },
        )

    monkeypatch.setattr(api, "token_valid", lambda: False)
    monkeypatch.setattr(api, "generate_token", fake_generate_token)
    monkeypatch.setattr(
        twitch.requests,
        "get",
        fake_get,
    )

    result = api.live("dherrerajdev")

    assert generated == [True]
    assert result.live is True
    assert result.title == "Live coding"
    assert result.category == "Software and Game Development"
    assert result.tags == ["python", "reflex"]
    assert result.viewer == 42
    assert calls == [
        (
            "https://api.twitch.tv/helix/streams",
            {"user_login": "dherrerajdev"},
            {
                "Client-ID": api.CLIENT_ID,
                "Authorization": "Bearer fresh-token",
            },
            twitch.REQUEST_TIMEOUT_SECONDS,
        )
    ]


def test_live_returns_offline_payload_when_stream_is_missing(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "existing-token"
    api.token_exp = 999

    monkeypatch.setattr(api, "token_valid", lambda: True)
    monkeypatch.setattr(
        twitch.requests,
        "get",
        lambda url, params, headers, timeout: StubResponse(200, {"data": []}),
    )

    result = api.live("dherrerajdev")

    assert result.live is False
    assert result.title is None
    assert result.category is None
    assert result.tags == []
    assert result.viewer == 0


def test_live_returns_offline_payload_for_incomplete_stream_payload(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "existing-token"
    api.token_exp = 999

    monkeypatch.setattr(api, "token_valid", lambda: True)
    monkeypatch.setattr(
        twitch.requests,
        "get",
        lambda url, params, headers, timeout: StubResponse(
            200,
            {
                "data": [
                    {
                        "title": " ",
                        "game_name": "Software and Game Development",
                        "tags": ["python"],
                        "viewer_count": 42,
                    }
                ]
            },
        ),
    )

    result = api.live("dherrerajdev")

    assert result.live is False
    assert result.title is None
    assert result.category is None


def test_live_filters_invalid_or_blank_tags(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "existing-token"
    api.token_exp = 999

    monkeypatch.setattr(api, "token_valid", lambda: True)
    monkeypatch.setattr(
        twitch.requests,
        "get",
        lambda url, params, headers, timeout: StubResponse(
            200,
            {
                "data": [
                    {
                        "title": "Live coding",
                        "game_name": "Software and Game Development",
                        "tags": ["python", " ", 123, "reflex"],
                        "viewer_count": 42,
                    }
                ]
            },
        ),
    )

    result = api.live("dherrerajdev")

    assert result.live is True
    assert result.tags == ["python", "reflex"]


def test_live_returns_offline_payload_on_request_failure(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "existing-token"
    api.token_exp = 999

    monkeypatch.setattr(api, "token_valid", lambda: True)

    def fake_get(url, params, headers, timeout):
        raise twitch.requests.RequestException("timeout")

    monkeypatch.setattr(twitch.requests, "get", fake_get)

    result = api.live("dherrerajdev")

    assert result == api._offline_live()


def test_live_logs_fail_closed_warning_on_request_failure(monkeypatch, caplog):
    api = twitch.TwitchAPI()
    api.token = "existing-token"
    api.token_exp = 999

    monkeypatch.setattr(api, "token_valid", lambda: True)

    def fake_get(url, params, headers, timeout):
        raise twitch.requests.RequestException("timeout")

    monkeypatch.setattr(twitch.requests, "get", fake_get)

    with caplog.at_level("WARNING"):
        result = api.live("dherrerajdev")

    assert result == api._offline_live()
    assert caplog.records[-1].message == "twitch_live_fetch_failed_closed"
    assert caplog.records[-1].event == "twitch_live_fetch_failed_closed"
    assert caplog.records[-1].integration == "twitch"
    assert caplog.records[-1].operation == "live"
    assert caplog.records[-1].fail_closed is True
    assert caplog.records[-1].error_type == "RequestException"


def test_live_returns_offline_payload_on_json_failure(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "existing-token"
    api.token_exp = 999

    class BrokenJsonResponse(StubResponse):
        def json(self) -> dict[str, Any]:
            raise ValueError("bad json")

    monkeypatch.setattr(api, "token_valid", lambda: True)
    monkeypatch.setattr(
        twitch.requests,
        "get",
        lambda url, params, headers, timeout: BrokenJsonResponse(200, {}),
    )

    result = api.live("dherrerajdev")

    assert result == api._offline_live()


def test_live_returns_offline_payload_on_runtime_failure(monkeypatch):
    api = twitch.TwitchAPI()
    api.token = "existing-token"
    api.token_exp = 999

    monkeypatch.setattr(api, "token_valid", lambda: True)
    monkeypatch.setattr(api, "_normalize_tags", lambda raw_value: 1 / 0)
    monkeypatch.setattr(
        twitch.requests,
        "get",
        lambda url, params, headers, timeout: StubResponse(
            200,
            {
                "data": [
                    {
                        "title": "Live coding",
                        "game_name": "Software and Game Development",
                        "tags": ["python"],
                        "viewer_count": 42,
                    }
                ]
            },
        ),
    )

    result = api.live("dherrerajdev")

    assert result == api._offline_live()
