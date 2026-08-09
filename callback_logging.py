"""Shared callbacks and logging utilities for all agents in this project.

Cloud Logging is opt-in so the project remains runnable locally and in CI
without requiring live Google Cloud credentials.
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse

logger = logging.getLogger("llm_auditor")


def configure_logging() -> None:
    if getattr(configure_logging, "_configured", False):
        return
    if os.getenv("ENABLE_CLOUD_LOGGING", "false").lower() == "true":
        try:
            import google.cloud.logging
            client = google.cloud.logging.Client()
            client.setup_logging()
            logger.info("Cloud Logging enabled.")
        except Exception:
            _configure_local_logging()
            logger.warning("Cloud Logging unavailable; using local structured logging.", exc_info=True)
    else:
        _configure_local_logging()
    configure_logging._configured = True


def _configure_local_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s :: %(message)s")


def _log_event(event_type: str, agent_name: str, payload: dict[str, Any]) -> None:
    record = {"event": event_type, "agent": agent_name, "timestamp": time.time(), **payload}
    logger.info(json.dumps(record, default=str))


def log_query_to_model(callback_context: CallbackContext, llm_request: LlmRequest) -> None:
    configure_logging()
    if llm_request.contents and llm_request.contents[-1].role == "user":
        parts = llm_request.contents[-1].parts
        if parts and parts[-1].text:
            _log_event("query_to_model", callback_context.agent_name, {"message": parts[-1].text})


def log_model_response(callback_context: CallbackContext, llm_response: LlmResponse) -> None:
    configure_logging()
    if not (llm_response.content and llm_response.content.parts):
        return
    for part in llm_response.content.parts:
        if part.text:
            _log_event("model_response", callback_context.agent_name, {"text": part.text})
        elif part.function_call:
            _log_event("tool_call", callback_context.agent_name, {"tool": part.function_call.name, "args": part.function_call.args})
