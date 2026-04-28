"""Pure domain logic for Magic Square operations."""

from __future__ import annotations

from magic_square.constants import EMPTY_CELL_VALUE, MATRIX_SIZE

Board = list[list[int]]
Coords = tuple[int, int]


def find_blank_coords(board: Board) -> list[Coords]:
    """Returns blank-cell coordinates in row-major order (1-indexed)."""
    blanks: list[Coords] = []

    for row_index, row in enumerate(board, start=1):
        for col_index, value in enumerate(row, start=1):
            if value == EMPTY_CELL_VALUE:
                blanks.append((row_index, col_index))

    return blanks


__all__ = ["MATRIX_SIZE", "find_blank_coords"]
