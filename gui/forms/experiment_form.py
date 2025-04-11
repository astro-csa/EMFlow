from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGroupBox
from base.experiment import Experiment
from gui.forms.program_form import ProgramForm

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

    def get_configs(self):
        return {
            form.program_class.name: form.get_config()
            for form in self.program_forms
        }
    
    def run_simulation(self):
        for form in self.program_forms:
            try:
                form.run_program()
            except Exception as e:
                print(f"[ERROR] Failed to run {form.program_class.name}: {e}")
    
    def _generate_config(self, form: ProgramForm):
        try:
            config = form.get_config
            program = form.program_class(config=config)
            program.generate_config()
            print(f"[SUCCESS] Config generated for {form.program_class.name}")
        except Exception as e:
            print(f"[ERROR] Failed to generate config: {e}")
