"""Manual CaseInput construction — same model as Excel import."""

from __future__ import annotations

from typing import Any

from pems.domain.case_input import CaseInput


def case_input_from_mapping(data: dict[str, Any], *, source_path: str | None = None) -> CaseInput:
    """Build CaseInput from a plain dict (UI form / API).

    Unknown keys go to extras. Known fields must match CaseInput attribute names.
    """
    known = set(CaseInput.field_names()) | {"source", "source_path", "extras"}
    kwargs: dict[str, Any] = {}
    extras: dict[str, Any] = {}
    for k, v in data.items():
        if k in known and k not in ("extras",):
            kwargs[k] = v
        else:
            extras[k] = v
    if "extras" in data and isinstance(data["extras"], dict):
        extras = {**extras, **data["extras"]}
    kwargs["extras"] = extras
    kwargs["source"] = "manual"
    kwargs["source_path"] = source_path
    return CaseInput(**kwargs)
