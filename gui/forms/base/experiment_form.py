from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGroupBox
from PyQt5.QtCore import QThreadPool
from base.experiment import Experiment
from gui.forms.base.program_form import ProgramForm
from gui.utils.tasks import SimulationTask
from typing import Type
from base.emsoft_program import EMSoftProgram

class ExperimentForm(QWidget):
    def __init__(self, experiment: Experiment):
        super().__init__()

        self.experiment = experiment
        self.program_forms = []  # List of ProgramForm instances

        main_layout = QVBoxLayout()
        program_layout = QHBoxLayout()

        for step_name, program_class, config in experiment.steps:
            form = ProgramForm(type(config), program_class)
            group = QGroupBox(step_name)
            group_layout = QVBoxLayout()

            group_layout.addWidget(form)

            group.setLayout(group_layout)

            self.program_forms.append(form)
            program_layout.addWidget(group)

        main_layout.addLayout(program_layout)

        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        main_layout.addWidget(self.run_button)

        self.setLayout(main_layout)
    
    def run_simulation(self):
        task = SimulationTask(self.experiment)
        QThreadPool.globalInstance().start(task)

