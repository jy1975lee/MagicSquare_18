"""Boundary layer for input validation and domain delegation."""

from __future__ import annotations

from magic_square.constants import MATRIX_SIZE

Board = list[list[int]]

E_INPUT_SIZE = "E_INPUT_SIZE"
E_DOMAIN_NO_SOLUTION = "E_DOMAIN_NO_SOLUTION"


def _build_error_message(code: str, detail: str) -> str:
    """Creates a consistent boundary error message schema."""
    return f"{code}: {detail}"


def validate(board: Board) -> None:
    """Validates boundary-level input shape contract (4x4)."""
    if len(board) != MATRIX_SIZE or any(len(row) != MATRIX_SIZE for row in board):
        raise ValueError(
            _build_error_message(
                E_INPUT_SIZE,
                f"input matrix must be {MATRIX_SIZE}x{MATRIX_SIZE}.",
            )
        )


def solve(board: Board) -> list[int]:
    """Delegates solving to domain layer.

    The domain solve logic is intentionally deferred to later TDD commits.
    """
    _ = board
    raise ValueError(
        _build_error_message(E_DOMAIN_NO_SOLUTION, "domain solve is not implemented yet.")
    )
