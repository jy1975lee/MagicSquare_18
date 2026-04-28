"""TRACK A — UI / Boundary RED (pytest).

Dual-Track RED only: no production imports until API exists.
Each test fails until Boundary implementation satisfies the contract.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from magic_square.boundary import E_INPUT_SIZE, validate


def test_ui_red_01_non_4x4_matrix_rejects_with_input_size_error() -> None:
    """UI-RED-01: non-4x4 input → E_INPUT_SIZE; solver not called."""
    # Arrange
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 0], [9, 10, 11]]

    # Act / Assert
    with pytest.raises(ValueError, match=E_INPUT_SIZE):
        validate(board)


def test_ui_red_02_wrong_empty_cell_count_rejects_with_empty_count_error() -> None:
    """UI-RED-02: zero count ≠ 2 → E_EMPTY_COUNT."""
    pytest.fail("RED: UI-RED-02 — Boundary not implemented")


def test_ui_red_03_value_out_of_range_rejects_with_value_range_error() -> None:
    """UI-RED-03: cell outside 0 or 1..16 → E_VALUE_RANGE."""
    pytest.fail("RED: UI-RED-03 — Boundary not implemented")


def test_ui_red_04_duplicate_nonzero_rejects_with_duplicate_error() -> None:
    """UI-RED-04: duplicate non-zero values → E_DUPLICATE_NONZERO."""
    pytest.fail("RED: UI-RED-04 — Boundary not implemented")


def test_ui_red_05_success_returns_length_six_array() -> None:
    """UI-RED-05: valid partial board → success int[6]."""
    pytest.fail("RED: UI-RED-05 — Boundary not implemented")


def test_ui_red_06_success_returns_one_indexed_coordinates() -> None:
    """UI-RED-06: success coordinates r,c in 1..4 (1-index)."""
    pytest.fail("RED: UI-RED-06 — Boundary not implemented")
