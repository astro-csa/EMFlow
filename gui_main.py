import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.forms.experiment_form import ExperimentForm
from gui.layout.simulation_selector import SimulationSelector
from simulations.simulation_registry import SIMULATIONS

from gui.forms.program_form import ProgramForm
from parameters.emmcopencl import EMMCOpenCLParameters
from programs.emmcopencl import EMMCOpenCL

class EMFlow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EMFlow – Configuration Generator")

        widget = SimulationSelector()
        self.setCentralWidget(widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EMFlow()
    window.show()

    app.exec_()
