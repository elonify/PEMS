"""Shared UI widgets — display only."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pems.presentation.view_models import DisplayRow, TableModel


def rows_table(rows: list[DisplayRow], *, show_source: bool = True) -> QTableWidget:
    cols = ["Label", "Value", "Unit", "Status"]
    if show_source:
        cols.append("Source")
    t = QTableWidget(len(rows), len(cols))
    t.setHorizontalHeaderLabels(cols)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    t.setAlternatingRowColors(True)
    for i, r in enumerate(rows):
        t.setItem(i, 0, QTableWidgetItem(r.label))
        val = QTableWidgetItem(r.display)
        if r.status == "unavailable":
            val.setToolTip(r.note or "Unavailable")
        elif r.note:
            val.setToolTip(r.note)
        t.setItem(i, 1, val)
        t.setItem(i, 2, QTableWidgetItem(r.unit))
        t.setItem(i, 3, QTableWidgetItem(r.status))
        if show_source:
            t.setItem(i, 4, QTableWidgetItem(r.source))
    return t


def model_table(model: TableModel) -> QWidget:
    w = QWidget()
    lay = QVBoxLayout(w)
    title = QLabel(f"<b>{model.title}</b>")
    lay.addWidget(title)
    t = QTableWidget(len(model.rows), len(model.columns))
    t.setHorizontalHeaderLabels(model.columns)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    t.setAlternatingRowColors(True)
    for i, row in enumerate(model.rows):
        for j, cell in enumerate(row):
            t.setItem(i, j, QTableWidgetItem(str(cell)))
    lay.addWidget(t)
    for n in model.notes:
        note = QLabel(n)
        note.setWordWrap(True)
        note.setStyleSheet("color: #555;")
        lay.addWidget(note)
    return w


def banner(text: str, *, kind: str = "info") -> QLabel:
    lab = QLabel(text)
    lab.setWordWrap(True)
    lab.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    if kind == "warn":
        lab.setStyleSheet(
            "background:#fff3cd; border:1px solid #ffc107; padding:8px; border-radius:4px;"
        )
    elif kind == "error":
        lab.setStyleSheet(
            "background:#f8d7da; border:1px solid #f5c2c7; padding:8px; border-radius:4px;"
        )
    else:
        lab.setStyleSheet(
            "background:#e7f1ff; border:1px solid #0d6efd; padding:8px; border-radius:4px;"
        )
    return lab
