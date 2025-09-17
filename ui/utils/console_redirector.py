from PyQt5.QtCore import QObject, pyqtSignal


class EmittingStream(QObject):
    """
    A custom stream class that emits text as a signal.

    This class is designed to redirect text output (e.g., from `stdout` or `stderr`)
    so that it can be displayed or processed in a PyQt5 GUI. By emitting text as a `pyqtSignal`,
    it allows the GUI to capture and display the output in real time.

    Attributes:
        - text_written (pyqtSignal): A signal that emits the written text as a string.

    Methods:
        - write(text): Emits the given text via the `text_written` signal.
        - flush(): Placeholder method (does nothing), included to maintain compatibility with stream interfaces.
    """

    # Define a PyQt5 signal that emits a string whenever text is written
    text_written = pyqtSignal(str)

    def write(self, text):
        """
        Emits the given text as a signal.

        This method is called when text is written to the stream (e.g., via `print()`).
        It emits the `text_written` signal with the provided text.

        Args:
            text (str): The text to emit.
        """
        self.text_written.emit(str(text))  # Emit the text as a signal

    def flush(self):
        """
        A placeholder method to maintain compatibility with standard stream interfaces.

        This method is necessary because streams (like `sys.stdout` and `sys.stderr`)
        often call `flush()` to ensure that all written data is output. In this case,
        the method does nothing, as the `write()` method directly emits the text.
        """
        pass
