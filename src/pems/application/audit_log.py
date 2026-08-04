"""Audit logging shell (stdlib logging)."""

from __future__ import annotations

import logging

logger = logging.getLogger("pems.audit")


def log_event(event: str, **fields: object) -> None:
    logger.info("%s %s", event, fields)
