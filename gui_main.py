import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow
from gui.utils.console_redirector import EmittingStream
from gui.widgets.console_widget import ConsoleWidget

from gui.layout.simulation_selector import SimulationSelector
from simulations.simulation_registry import SIMULATIONS

class EMFlow(QMainWindow):
    def __init__(self, console_widget):
        super().__init__()
        self.setWindowTitle("EMFlow - Configuration Generator")

        self.main_layout = QVBoxLayout()

        self.widget = SimulationSelector(console_widget)
        self.main_layout.addWidget(self.widget)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    console_widget = ConsoleWidget()

    stream = EmittingStream()
    stream.text_written.connect(console_widget.append)

    #sys.stdout = stream
    #sys.stderr = stream

    window = EMFlow(console_widget)
    window.showMaximized()

    app.exec_()
