"""Base protocol for calculation modules."""

from __future__ import annotations

from typing import Any, Protocol

from pems.core.exceptions import NotImplementedCalculationError
from pems.domain.case_input import CaseInput


class CalculationModule(Protocol):
    name: str
    contract_path: str

    def run(self, case: CaseInput, upstream: dict[str, Any]) -> dict[str, Any]:
        ...


class UnimplementedModule:
    """Scaffold module that refuses to invent formulas."""

    name: str = "unimplemented"
    contract_path: str = ""

    def run(self, case: CaseInput, upstream: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedCalculationError(
            f"Module {self.name!r} not implemented. Contract: {self.contract_path}"
        )
