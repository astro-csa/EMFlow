from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QPushButton, QHBoxLayout
from gui.forms.experiment_form import ExperimentForm
from simulations.simulation_registry import SIMULATIONS

class SimulationSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget()
        self.stacked_widget = QStackedWidget()

        self.list_widget.setMaximumWidth(150)
        self.list_widget.setMinimumWidth(100)

        for name in SIMULATIONS.keys():
            self.list_widget.addItem(name)

        for experiment in SIMULATIONS.values():
            form = ExperimentForm(experiment)
            self.stacked_widget.addWidget(form)

        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        layout = QHBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)