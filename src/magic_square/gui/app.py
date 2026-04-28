"""PyQt6 screen (UI) for the Magic Square boundary workflow."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from magic_square.boundary import solve, validate
from magic_square.constants import MATRIX_SIZE

Board = list[list[int]]


class MagicSquareWindow(QMainWindow):
    """MVP screen for entering a 4x4 board and invoking boundary use flow."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Magic Square 4x4")
        self._cells: list[list[QLineEdit]] = []
        self._result_label = QLabel("결과: (아직 없음)")
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        for row_index in range(MATRIX_SIZE):
            row_cells: list[QLineEdit] = []
            for col_index in range(MATRIX_SIZE):
                cell = QLineEdit("0")
                cell.setMaxLength(2)
                cell.setFixedWidth(44)
                grid_layout.addWidget(cell, row_index, col_index)
                row_cells.append(cell)
            self._cells.append(row_cells)

        button_layout = QHBoxLayout()
        solve_button = QPushButton("풀기")
        solve_button.clicked.connect(self._on_solve_clicked)
        button_layout.addWidget(solve_button)

        root_layout.addLayout(grid_layout)
        root_layout.addLayout(button_layout)
        root_layout.addWidget(self._result_label)
        root.setLayout(root_layout)
        self.setCentralWidget(root)

    def _read_board(self) -> Board:
        board: Board = []
        for row_index in range(MATRIX_SIZE):
            row: list[int] = []
            for col_index in range(MATRIX_SIZE):
                raw_text = self._cells[row_index][col_index].text().strip()
                text = raw_text if raw_text else "0"
                try:
                    value = int(text)
                except ValueError as error:
                    raise ValueError("각 칸은 정수여야 합니다.") from error
                row.append(value)
            board.append(row)
        return board

    def _on_solve_clicked(self) -> None:
        try:
            board = self._read_board()
            validate(board)
            result = solve(board)
            self._result_label.setText(f"결과: {result}")
        except ValueError as error:
            QMessageBox.warning(self, "입력/해결 오류", str(error))


def run() -> int:
    """Runs the PyQt6 GUI application."""
    app = QApplication(sys.argv)
    window = MagicSquareWindow()
    window.show()
    return app.exec()
