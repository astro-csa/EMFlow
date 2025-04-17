from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton
from gui.forms.program_form import ProgramForm
from gui.utils.get_programs import get_programs

# This import is only to ensure that all programs and parameters are imported so PyInstaller can bundle them properly
import simulations.simulation_registry

class AllProgramsForm(QWidget):
    def __init__(self):
        super().__init__()

        self.available_programs = get_programs()  # List of (config_class, program_class, name)
        self.program_forms = {}  # name -> ProgramForm

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        for config_class, program_class, name in self.available_programs:
            form = ProgramForm(config_class,program_class)
            self.program_forms[name] = form
            self.tabs.addTab(form, name)

        layout.addWidget(self.tabs)

        self.generate_button = QPushButton("Generate Configs")
        self.generate_button.clicked.connect(self.generate_all_configs)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    # Deprecated
    def generate_all_configs(self):
        for name, form in self.program_forms.items():
            try:
                config = form.get_config()
                program_instance = form.program_class(config=config)
                program_instance.generate_config()
            except Exception as e:
                print(f"[ERROR] Failed to generate config for {name}: {e}")
