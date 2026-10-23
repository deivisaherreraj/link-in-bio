import json
import logging
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import TextIO

APPLICATION_LOGGER_NAME = "website_frontend"
_HANDLER_MARKER = "_website_frontend_json"
_SAFE_CONTEXT_TYPES: dict[str, tuple[type[object], ...]] = {
    "error_type": (str,),
    "key": (str,),
    "reason": (str,),
    "status_code": (int,),
}
_FAIL_CLOSED_FIELD_TYPES: dict[str, type[object]] = {
    "event": str,
    "integration": str,
    "operation": str,
    "fail_closed": bool,
}


def _safe_context(context: Mapping[str, object] | None) -> dict[str, object]:
    if context is None:
        return {}

    safe_context: dict[str, object] = {}
    for key, expected_types in _SAFE_CONTEXT_TYPES.items():
        value = context.get(key)
        if type(value) in expected_types:
            safe_context[key] = value

    return safe_context


def _safe_text(value: object, fallback: str) -> str:
    if isinstance(value, str):
        return value

    try:
        return str(value)
    except Exception:
        return fallback


class ApplicationJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        try:
            timestamp = datetime.fromtimestamp(record.created, tz=UTC).isoformat()
            payload: dict[str, object] = {
                "timestamp": timestamp,
                "level": _safe_text(record.levelname, "UNKNOWN"),
                "logger": _safe_text(record.name, APPLICATION_LOGGER_NAME),
                "message": self._safe_message(record),
            }

            for field, expected_type in _FAIL_CLOSED_FIELD_TYPES.items():
                value = getattr(record, field, None)
                if type(value) is expected_type:
                    payload[field] = value

            payload.update(_safe_context(record.__dict__))
            return json.dumps(
                payload,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            )
        except Exception:
            return (
                '{"timestamp":null,"level":"ERROR",'
                '"logger":"website_frontend.observability",'
                '"message":"log_serialization_failed"}'
            )

    @staticmethod
    def _safe_message(record: logging.LogRecord) -> str:
        try:
            return record.getMessage()
        except Exception:
            return "<unprintable>"


def configure_application_logging(*, stream: TextIO | None = None) -> None:
    application_logger = logging.getLogger(APPLICATION_LOGGER_NAME)
    if any(
        getattr(handler, _HANDLER_MARKER, False)
        for handler in application_logger.handlers
    ):
        return

    handler = logging.StreamHandler(stream)
    handler.setFormatter(ApplicationJsonFormatter())
    setattr(handler, _HANDLER_MARKER, True)
    application_logger.addHandler(handler)
    application_logger.setLevel(logging.INFO)
    application_logger.propagate = False


def fail_closed_event(
    *,
    event: str,
    integration: str,
    operation: str,
    context: Mapping[str, object] | None = None,
) -> dict[str, object]:
    return {
        **_safe_context(context),
        "event": event,
        "integration": integration,
        "operation": operation,
        "fail_closed": True,
    }


def log_fail_closed_event(
    logger: logging.Logger,
    *,
    event: str,
    integration: str,
    operation: str,
    context: Mapping[str, object] | None = None,
) -> None:
    logger.warning(
        event,
        extra=fail_closed_event(
            event=event,
            integration=integration,
            operation=operation,
            context=context,
        ),
    )
