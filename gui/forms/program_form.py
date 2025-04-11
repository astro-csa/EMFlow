from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton
from dataclasses import is_dataclass, fields  
from gui.forms.dataclass_form import DataclassForm


class ProgramForm(QWidget):
    def __init__(self, config_class, program_class):
        super().__init__()

        self.config_class = config_class
        self.program_class = program_class
        self.form_widgets = {}  # {"nml": DataclassForm, "bethe": DataclassForm, ...}

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        for field_ in fields(config_class):
            if not field_.init:
                continue

            field_name = field_.name 
            field_type = field_.type

            if is_dataclass(field_type):
                form = DataclassForm(field_type)
                self.form_widgets[field_name] = form
                self.tabs.addTab(form, field_name.upper())


        layout.addWidget(self.tabs)

        self.generate_button = QPushButton("Generate Config")
        self.generate_button.clicked.connect(self.generate_config)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate_config(self):
        try:
            config = self._get_config()
            program = self.program_class(config=config)
            program.generate_config()
        except Exception as e:
            print(f"[ERROR] Failed to generate config: {e}")

    def run_program(self):
        try:
            config = self._get_config()
            program = self.program_class(config=config)
            print(f"program.copy_input: {program.copy_input}")
            if program.copy_input:
                print("program.copy_input: True")
                program.copy_output_file(program.copy_input)
            program.run()
        except Exception as e:
            print(f"[ERROR]")

    def _get_config(self):
        """Devuelve un nuevo objeto de configuración con los valores del formulario."""
        updated_config_data = {}

        for key, form in self.form_widgets.items():
            updated_config_data[key] = form.get_instance()

        # Creamos una nueva instancia del objeto de configuración original
        return self.config_class(**updated_config_data)
