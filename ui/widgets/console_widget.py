from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit


class ConsoleWidget(QTextEdit):
    """
    A custom console widget for displaying logs, messages, or simulation output in the application.

    This widget is a specialized `QTextEdit` that is styled to resemble a terminal/console.
    It is read-only and supports appending text dynamically, making it ideal for use as a log or output display.

    Features:
        - Styled with a dark theme resembling a developer console.
        - Read-only by default to prevent user edits.
        - Monospaced font for better readability of logs/output.
    """

    def __init__(self, parent=None):
        """
        Initializes the `ConsoleWidget` with custom styles and properties.

        Args:
            parent (QWidget | None): The parent widget, if any.
        """
        super().__init__(parent)

        # Set the widget to read-only (no user edits allowed)
        self.setReadOnly(True)

        # Disable focus, ensuring the console does not receive input focus
        self.setFocusPolicy(Qt.NoFocus)

        # Set the font to a monospaced font for better alignment of log/output text
        self.setFont(QFont("Consolas", 10))

        # Set a minimum width to ensure proper visual alignment in the layout
        self.setMinimumWidth(400)

        # Apply custom styles using CSS to give the console a dark-themed appearance
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;  /* Dark background */
                color: #d4d4d4;  /* Light gray text for contrast */
                font-family: Consolas, monospace;  /* Monospaced font for developer-like appearance */
                font-size: 12px;  /* Slightly larger, readable font */
                padding: 6px;  /* Padding for better spacing */
                border: 1px solid #555;  /* Subtle border for separation */
            }
        """)

        # Add an initial message to the console
        self.append(">> EMFlow Console Initialized.\n")  # Inform the user that the console is ready
