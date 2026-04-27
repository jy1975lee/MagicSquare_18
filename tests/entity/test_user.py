"""Tests for MagicSquare User entity."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from magic_square.entity import User


def test_user_creation_with_valid_values() -> None:
    """Creates a user with valid identity fields."""
    # Arrange
    user_id = "u-1004"
    display_name = "Magic Tester"

    # Act
    user = User(user_id=user_id, display_name=display_name)

    # Assert
    assert user.user_id == user_id
    assert user.display_name == display_name


def test_user_creation_raises_when_user_id_is_blank() -> None:
    """Rejects blank user id values."""
    # Arrange
    display_name = "Magic Tester"

    # Act / Assert
    with pytest.raises(ValueError, match="user_id must not be empty."):
        User(user_id="   ", display_name=display_name)


def test_validate_board_input_accepts_valid_board() -> None:
    """Accepts a valid 4x4 board with two empty cells."""
    # Arrange
    user = User(user_id="u-1004", display_name="Magic Tester")
    board = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 0],
        [4, 14, 0, 1],
    ]

    # Act
    user.validate_board_input(board)

    # Assert
    assert True


def test_validate_board_input_rejects_non_4x4_shape() -> None:
    """Rejects board shapes other than 4x4."""
    # Arrange
    user = User(user_id="u-1004", display_name="Magic Tester")
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 0], [9, 10, 11]]

    # Act / Assert
    with pytest.raises(ValueError, match="each board row must have exactly 4 columns."):
        user.validate_board_input(board)


def test_validate_board_input_rejects_out_of_range_values() -> None:
    """Rejects values outside 0..16."""
    # Arrange
    user = User(user_id="u-1004", display_name="Magic Tester")
    board = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, -1, 0],
        [4, 14, 0, 1],
    ]

    # Act / Assert
    with pytest.raises(ValueError, match="board values must be in range 0..16."):
        user.validate_board_input(board)


def test_validate_board_input_rejects_non_zero_duplicates() -> None:
    """Rejects duplicated non-zero values."""
    # Arrange
    user = User(user_id="u-1004", display_name="Magic Tester")
    board = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 0],
        [4, 14, 6, 0],
    ]

    # Act / Assert
    with pytest.raises(ValueError, match="non-zero board values must be unique."):
        user.validate_board_input(board)


def test_validate_board_input_rejects_wrong_empty_cell_count() -> None:
    """Rejects boards where zero count is not exactly two."""
    # Arrange
    user = User(user_id="u-1004", display_name="Magic Tester")
    board = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]

    # Act / Assert
    with pytest.raises(
        ValueError, match="board must contain exactly two empty cells \\(0\\)."
    ):
        user.validate_board_input(board)

