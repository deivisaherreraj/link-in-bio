import io
import json
import logging

from website_frontend.integrations.observability import (
    configure_application_logging,
    fail_closed_event,
    log_fail_closed_event,
)


def test_fail_closed_event_payload_remains_compatible():
    assert fail_closed_event(
        event="example_failed_closed",
        integration="example",
        operation="fetch",
        context={"error_type": "RuntimeError"},
    ) == {
        "event": "example_failed_closed",
        "integration": "example",
        "operation": "fetch",
        "fail_closed": True,
        "error_type": "RuntimeError",
    }


def test_log_fail_closed_event_emits_structured_warning(caplog):
    logger = logging.getLogger("test.observability")

    with caplog.at_level("WARNING", logger=logger.name):
        result = log_fail_closed_event(
            logger,
            event="example_failed_closed",
            integration="example",
            operation="fetch",
            context={"error_type": "RuntimeError"},
        )

    assert result is None
    record = caplog.records[-1]
    assert record.message == "example_failed_closed"
    assert record.event == "example_failed_closed"
    assert record.integration == "example"
    assert record.operation == "fetch"
    assert record.fail_closed is True
    assert record.error_type == "RuntimeError"


def test_configured_application_logger_emits_one_line_json():
    stream = io.StringIO()
    application_logger = logging.getLogger("website_frontend")
    original_handlers = application_logger.handlers[:]
    original_level = application_logger.level
    original_propagate = application_logger.propagate

    try:
        configure_application_logging(stream=stream)

        log_fail_closed_event(
            logging.getLogger("website_frontend.integrations.example"),
            event="example_failed_closed",
            integration="example",
            operation="fetch",
            context={"error_type": "RuntimeError", "status_code": 503},
        )
    finally:
        application_logger.handlers = original_handlers
        application_logger.setLevel(original_level)
        application_logger.propagate = original_propagate

    lines = stream.getvalue().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload == {
        "timestamp": payload["timestamp"],
        "level": "WARNING",
        "logger": "website_frontend.integrations.example",
        "message": "example_failed_closed",
        "event": "example_failed_closed",
        "integration": "example",
        "operation": "fetch",
        "fail_closed": True,
        "error_type": "RuntimeError",
        "status_code": 503,
    }


def test_configure_application_logging_is_idempotent():
    stream = io.StringIO()
    application_logger = logging.getLogger("website_frontend")
    original_handlers = application_logger.handlers[:]
    original_level = application_logger.level
    original_propagate = application_logger.propagate

    try:
        configure_application_logging(stream=stream)
        configure_application_logging(stream=stream)

        logging.getLogger("website_frontend.example").info("configured_once")

        configured_handlers = [
            handler
            for handler in application_logger.handlers
            if getattr(handler, "_website_frontend_json", False)
        ]
    finally:
        application_logger.handlers = original_handlers
        application_logger.setLevel(original_level)
        application_logger.propagate = original_propagate

    assert len(configured_handlers) == 1
    assert len(stream.getvalue().splitlines()) == 1


def test_fail_closed_context_cannot_override_reserved_fields():
    payload = fail_closed_event(
        event="example_failed_closed",
        integration="example",
        operation="fetch",
        context={
            "event": "forged_event",
            "integration": "forged_integration",
            "operation": "forged_operation",
            "fail_closed": False,
            "timestamp": "forged_timestamp",
            "level": "DEBUG",
            "logger": "forged.logger",
            "message": "forged_message",
            "reason": "timeout",
        },
    )

    assert payload == {
        "event": "example_failed_closed",
        "integration": "example",
        "operation": "fetch",
        "fail_closed": True,
        "reason": "timeout",
    }


def test_json_output_filters_secrets_payloads_and_unexpected_values():
    stream = io.StringIO()
    application_logger = logging.getLogger("website_frontend")
    original_handlers = application_logger.handlers[:]
    original_level = application_logger.level
    original_propagate = application_logger.propagate
    secret = "never-serialize-this-secret"

    try:
        configure_application_logging(stream=stream)

        log_fail_closed_event(
            logging.getLogger("website_frontend.integrations.example"),
            event="example_failed_closed",
            integration="example",
            operation="fetch",
            context={
                "error_type": "RuntimeError",
                "status_code": object(),
                "credentials": secret,
                "payload": {"token": secret},
                "exception": RuntimeError(secret),
                "unknown": secret,
            },
        )
    finally:
        application_logger.handlers = original_handlers
        application_logger.setLevel(original_level)
        application_logger.propagate = original_propagate

    rendered = stream.getvalue()
    payload = json.loads(rendered)
    assert secret not in rendered
    assert payload["error_type"] == "RuntimeError"
    assert "status_code" not in payload
    assert "credentials" not in payload
    assert "payload" not in payload
    assert "exception" not in payload
    assert "unknown" not in payload
