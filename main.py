import sys
import traceback

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    # Create the PyQt application object
    app = QApplication(sys.argv)

    # Create and display the main application window
    window = MainWindow()
    window.showMaximized()  # Show the window maximized

    # Run the application event loop
    try:
        app.exec_()
    except Exception:
        # Catch and print any exceptions that occur during the application runtime
        traceback.print_exc()
        print("Press return to exit.")
        input()
