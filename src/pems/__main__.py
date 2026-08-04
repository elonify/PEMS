"""CLI entry — Phase 0 reports scaffold status only."""

from __future__ import annotations


def main() -> None:
    from pems import __spec_status__, __version__, __numerical_validated__

    print(f"pems {__version__}")
    print(f"status: {__spec_status__}")
    print(f"numerical_validated: {__numerical_validated__}")
    print("No economic calculations are implemented in Phase 0.")


if __name__ == "__main__":
    main()
