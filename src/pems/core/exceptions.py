"""Shared exceptions."""


class PemsError(Exception):
    """Base PEMS error."""


class NotImplementedCalculationError(PemsError):
    """Raised when a calculation module is scaffolded but not yet implemented.

    Implementations must follow docs/02_SPECIFICATIONS/modules/* contracts
    and the approved Golden Master — do not invent formulas.
    """


class ValidationError(PemsError):
    """CaseInput or import validation failure."""


class GoldenMasterError(PemsError):
    """Golden Master path/hash/read failure."""
