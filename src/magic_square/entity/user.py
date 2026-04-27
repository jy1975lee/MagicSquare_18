"""User entity for MagicSquare domain rules."""

from __future__ import annotations

from dataclasses import dataclass

Board = list[list[int]]
BOARD_SIZE = 4
MIN_VALUE = 0
MAX_VALUE = 16
EMPTY_CELL_VALUE = 0
EXPECTED_EMPTY_CELLS = 2


@dataclass(frozen=True, slots=True)
class User:
    """Represents a user who submits MagicSquare board inputs.

    The entity only performs domain-level validation for user-provided boards.
    It does not manage UI, I/O, or orchestration concerns.

    Attributes:
        user_id: Unique identifier of the user.
        display_name: Human-readable user name.
    """

    user_id: str
    display_name: str

    def __post_init__(self) -> None:
        """Validates invariant constraints for the user entity.

        Raises:
            ValueError: If `user_id` or `display_name` is empty or blank.
        """
        if not self.user_id.strip():
            raise ValueError("user_id must not be empty.")
        if not self.display_name.strip():
            raise ValueError("display_name must not be empty.")

    def validate_board_input(self, board: Board) -> None:
        """Validates a 4x4 MagicSquare input board.

        Validation rules:
            - Board must be exactly 4x4.
            - Every value must be in range 0..16.
            - Value `0` must appear exactly two times.
            - Non-zero values must not contain duplicates.

        Args:
            board: 4x4 board data submitted by the user.

        Raises:
            ValueError: If board shape or values violate domain constraints.
        """
        self._validate_board_shape(board)
        self._validate_value_range(board)
        self._validate_empty_cell_count(board)
        self._validate_non_zero_uniqueness(board)

    @staticmethod
    def _validate_board_shape(board: Board) -> None:
        if len(board) != BOARD_SIZE:
            raise ValueError("board must have exactly 4 rows.")

        if any(len(row) != BOARD_SIZE for row in board):
            raise ValueError("each board row must have exactly 4 columns.")

    @staticmethod
    def _validate_value_range(board: Board) -> None:
        for row in board:
            for value in row:
                if value < MIN_VALUE or value > MAX_VALUE:
                    raise ValueError("board values must be in range 0..16.")

    @staticmethod
    def _validate_empty_cell_count(board: Board) -> None:
        empty_count = sum(
            1 for row in board for value in row if value == EMPTY_CELL_VALUE
        )
        if empty_count != EXPECTED_EMPTY_CELLS:
            raise ValueError("board must contain exactly two empty cells (0).")

    @staticmethod
    def _validate_non_zero_uniqueness(board: Board) -> None:
        non_zero_values = [value for row in board for value in row if value != 0]
        if len(non_zero_values) != len(set(non_zero_values)):
            raise ValueError("non-zero board values must be unique.")

