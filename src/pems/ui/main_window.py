"""PEMS main window — Phase 1H first-slice shell.

Navigation: Home/RESULTS · Case · Law · Production · Costs · Fiscal ·
Cash Flow · Results · Validation · Reports
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from pems.application.run_service import RunBundle, RunService
from pems.presentation.view_models import PresentationBundle, build_presentation
from pems.ui.widgets import banner, model_table, rows_table

NAV_PAGES = [
    ("home", "Home / RESULTS"),
    ("case", "Case"),
    ("law", "Law"),
    ("production", "Production"),
    ("costs", "Costs"),
    ("fiscal", "Fiscal"),
    ("cashflow", "Cash Flow"),
    ("results", "Results"),
    ("validation", "Validation"),
    ("reports", "Reports"),
]


class MainWindow(QMainWindow):
    def __init__(self, repo_root: Path | None = None) -> None:
        super().__init__()
        self.repo_root = repo_root or Path.cwd()
        self.service = RunService()
        self.bundle: RunBundle | None = None
        self.pres: PresentationBundle | None = None

        self.setWindowTitle("PEMS — Petroleum Economics Modeling System")
        self.resize(1200, 800)

        self._build_toolbar()
        self._build_body()
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Load case from Golden Master or run empty scaffold.")

        self._pages: dict[str, QWidget] = {}
        for key, _label in NAV_PAGES:
            page = QWidget()
            page.setLayout(QVBoxLayout())
            self._pages[key] = page
            self.stack.addWidget(page)

        self.nav.setCurrentRow(0)
        self._show_idle_home()

    def _build_toolbar(self) -> None:
        tb = QToolBar("Main")
        tb.setMovable(False)
        self.addToolBar(tb)
        act_load = QAction("Load GM case & Run", self)
        act_load.triggered.connect(self.load_and_run_gm)
        tb.addAction(act_load)
        act_about = QAction("About claims", self)
        act_about.triggered.connect(self._show_claims)
        tb.addAction(act_about)

    def _build_body(self) -> None:
        split = QSplitter()
        self.nav = QListWidget()
        self.nav.setFixedWidth(180)
        font = QFont()
        font.setPointSize(10)
        self.nav.setFont(font)
        for key, label in NAV_PAGES:
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.nav.addItem(item)
        self.nav.currentRowChanged.connect(self._on_nav)
        self.stack = QStackedWidget()
        split.addWidget(self.nav)
        split.addWidget(self.stack)
        split.setStretchFactor(1, 1)
        self.setCentralWidget(split)

    def _on_nav(self, row: int) -> None:
        if row < 0:
            return
        self.stack.setCurrentIndex(row)
        if self.pres is not None:
            self._render_all()

    def _clear_layout(self, w: QWidget) -> None:
        lay = w.layout()
        while lay.count():
            item = lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _scroll_wrap(self, inner: QWidget) -> QScrollArea:
        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setWidget(inner)
        return sc

    def _show_idle_home(self) -> None:
        page = self._pages["home"]
        self._clear_layout(page)
        lay = page.layout()
        lay.addWidget(
            banner(
                "PEMS Phase 1H first-slice presentation. "
                "Use <b>Load GM case &amp; Run</b> to import the approved Golden Master "
                "CaseInput (read-only) and display calculation outputs. "
                "Charts, Sensitivity, and Monte Carlo are <b>DEFERRED</b>.",
                kind="info",
            )
        )
        lay.addWidget(
            QLabel(
                "<p><b>Architecture:</b> UI → RunService → calculation modules → presentation view models.</p>"
                "<p>No NPV/IRR/production/cost formulas are evaluated in the UI layer.</p>"
            )
        )
        lay.addStretch(1)

    def load_and_run_gm(self) -> None:
        try:
            self.statusBar().showMessage("Importing Golden Master CaseInput (read-only)…")
            self.bundle = self.service.run_from_active_gm(self.repo_root)
            self.pres = build_presentation(self.bundle)
            self._render_all()
            self.statusBar().showMessage(
                f"Run complete. Equity={self.bundle.case.equity_share_company_1}; "
                f"validation issues={len(self.bundle.validation_errors)}"
            )
        except Exception as exc:  # noqa: BLE001 — surface to user
            QMessageBox.critical(self, "Run failed", str(exc))
            self.statusBar().showMessage(f"Run failed: {exc}")

    def _render_all(self) -> None:
        assert self.pres is not None
        p = self.pres

        def fill(key: str, title: str, rows_or_builder) -> None:
            page = self._pages[key]
            self._clear_layout(page)
            lay = page.layout()
            lay.addWidget(QLabel(f"<h2>{title}</h2>"))
            for b in p.deferred_banners:
                if key in ("home", "results", "reports"):
                    lay.addWidget(banner(b, kind="warn"))
            if callable(rows_or_builder):
                lay.addWidget(self._scroll_wrap(rows_or_builder()))
            else:
                inner = QWidget()
                il = QVBoxLayout(inner)
                if key == "home":
                    il.addWidget(
                        banner(
                            "Executive KPIs from RESULTS Equity (authoritative calc outputs).",
                            kind="info",
                        )
                    )
                il.addWidget(rows_table(rows_or_builder))
                # show IRR unavailable notes
                for r in rows_or_builder:
                    if r.status == "unavailable" and r.note:
                        il.addWidget(banner(f"{r.label}: {r.note}", kind="error"))
                lay.addWidget(self._scroll_wrap(inner))

        fill("home", "Home / RESULTS — Executive KPIs", p.results_kpi_rows)
        fill("case", "Case / Assumptions", p.case_rows)
        fill("law", "Fiscal Law Table (read-only)", p.law_rows)
        fill("production", "Production", lambda: model_table(p.production_table))
        fill("costs", "Costs", lambda: model_table(p.costs_table))
        fill("fiscal", "Fiscal / FLGT", lambda: model_table(p.fiscal_table))
        fill("cashflow", "Cash Flow / CR-NCF", lambda: model_table(p.cashflow_table))
        fill("results", "Results Equity KPIs", p.results_kpi_rows)
        fill("validation", "Validation", p.validation_rows)
        fill("reports", "Reports (dataset view)", p.reports_rows)

    def _show_claims(self) -> None:
        QMessageBox.information(
            self,
            "Claim discipline",
            "PRESENTATION SPECIFICATION READY = YES\n"
            "PRESENTATION FIRST SLICE = IMPLEMENTED (this UI)\n"
            "PRESENTATION NUMERICALLY VALIDATED = NOT CLAIMED\n"
            "FULL WORKBOOK PRESENTATION PARITY = NOT CLAIMED\n"
            "CHART PARITY = NOT CLAIMED\n"
            "RESULTS FULL INDEPENDENT VALIDATED = NOT CLAIMED\n"
            "Sensitivity / Monte Carlo = DEFERRED\n"
            "Golden Master = READ-ONLY",
        )


def run_app(repo_root: Path | None = None) -> int:
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication.instance() or QApplication(sys.argv)
    win = MainWindow(repo_root=repo_root)
    win.show()
    return app.exec()
