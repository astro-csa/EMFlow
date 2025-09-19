from __future__ import annotations

from collections.abc import Callable
from typing import Optional

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QAction, QMenu, QMenuBar


class MenuBar(QMenuBar):
    """Application menu bar containing Help and Tools menus."""

    def __init__(
        self,
        parent=None,
        *,
        on_modify_defaults: Optional[Callable[[], None]] = None,
        on_restore_defaults: Optional[Callable[[], None]] = None,
        wiki_url: str = "https://example.com/wiki",
    ) -> None:
        super().__init__(parent)
        self._on_modify_defaults = on_modify_defaults
        self._on_restore_defaults = on_restore_defaults
        self._wiki_url = wiki_url

        self._build_help_menu()
        self._build_tools_menu()

    def _build_help_menu(self) -> None:
        help_menu: QMenu = self.addMenu("Help")

        open_wiki_action = QAction("Open Wiki", self)
        open_wiki_action.triggered.connect(self._open_wiki)
        help_menu.addAction(open_wiki_action)

    def _build_tools_menu(self) -> None:
        tools_menu: QMenu = self.addMenu("Tools")

        modify_defaults_action = QAction("Modify Default Values", self)
        modify_defaults_action.triggered.connect(self._handle_modify_defaults)
        tools_menu.addAction(modify_defaults_action)

        restore_defaults_action = QAction("Restore Original Values", self)
        restore_defaults_action.triggered.connect(self._handle_restore_defaults)
        tools_menu.addAction(restore_defaults_action)

    def _open_wiki(self) -> None:
        QDesktopServices.openUrl(QUrl(self._wiki_url))

    def _handle_modify_defaults(self) -> None:
        if callable(self._on_modify_defaults):
            self._on_modify_defaults()

    def _handle_restore_defaults(self) -> None:
        if callable(self._on_restore_defaults):
            self._on_restore_defaults()
