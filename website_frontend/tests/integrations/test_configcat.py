import json
from typing import Any

from website_frontend.integrations.configcat import ConfigCatAPI


class StubConfigCatClient:
    def __init__(self, values: dict[str, Any]) -> None:
        self.values = values
        self.calls: list[tuple[str, str]] = []

    def get_value(self, key: str, default: str) -> Any:
        self.calls.append((key, default))
        return self.values.get(key, default)


class RaisingConfigCatClient:
    def __init__(self, error: Exception) -> None:
        self.error = error

    def get_value(self, key: str, default: str) -> Any:
        raise self.error


def test_schedule_parses_json_payload():
    schedule_payload = {"0": "18:00", "2": "20:30"}
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = StubConfigCatClient(
        {"live_schedule": json.dumps(schedule_payload)}
    )

    result = configcat_api.schedule()

    assert result == schedule_payload
    assert configcat_api.configcat.calls == [("live_schedule", "")]


def test_schedule_filters_invalid_keys_and_values():
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = StubConfigCatClient(
        {
            "live_schedule": json.dumps(
                {
                    "0": "18:00",
                    "2": " 20:30 ",
                    "7": "19:00",
                    "x": "21:00",
                    "3": "",
                    "4": "not-a-time",
                }
            )
        }
    )

    result = configcat_api.schedule()

    assert result == {"0": "18:00", "2": "20:30"}


def test_schedule_returns_empty_dict_when_client_is_missing():
    configcat_api = ConfigCatAPI()
    if hasattr(configcat_api, "configcat"):
        delattr(configcat_api, "configcat")

    result = configcat_api.schedule()

    assert result == {}


def test_schedule_returns_empty_dict_for_invalid_json_payload():
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = StubConfigCatClient({"live_schedule": "not-json"})

    result = configcat_api.schedule()

    assert result == {}
    assert configcat_api.configcat.calls == [("live_schedule", "")]


def test_schedule_returns_empty_dict_for_non_mapping_json_payload():
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = StubConfigCatClient({"live_schedule": '["18:00"]'})

    result = configcat_api.schedule()

    assert result == {}


def test_schedule_returns_empty_dict_for_non_string_value():
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = StubConfigCatClient({"live_schedule": {"0": "18:00"}})

    result = configcat_api.schedule()

    assert result == {}
    assert configcat_api.configcat.calls == [("live_schedule", "")]


def test_schedule_fails_closed_when_get_value_raises(caplog):
    configcat_api = ConfigCatAPI()
    configcat_api.configcat = RaisingConfigCatClient(RuntimeError("boom"))

    with caplog.at_level("WARNING"):
        result = configcat_api.schedule()

    assert result == {}
    assert caplog.records[-1].message == "configcat_get_value_failed_closed"
    assert caplog.records[-1].event == "configcat_get_value_failed_closed"
    assert caplog.records[-1].integration == "configcat"
    assert caplog.records[-1].operation == "get_value"
    assert caplog.records[-1].fail_closed is True
    assert caplog.records[-1].key == "live_schedule"
    assert caplog.records[-1].error_type == "RuntimeError"
