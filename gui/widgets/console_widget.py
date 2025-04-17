from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ConsoleWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setFont(QFont("Consolas", 10))
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 12px;
                padding: 6px;
                border: 1px solid #555;
            }
        """)

        self.append(">> EMFlow Console Initialized.\n")