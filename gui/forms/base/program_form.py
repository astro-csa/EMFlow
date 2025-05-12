from dataclasses import is_dataclass, fields
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton
from gui.forms.base.dataclass_form import DataclassForm
from gui.forms.programs.emecci_foil_form import FoilForm
from gui.forms.programs.emecci_defect_form import DefectForm
from base.emsoft_program import EMSoftProgram
from typing import Type

class ProgramForm(QWidget):
    """
    Parameter class structure:

    @dataclass
    class ProgramParameters:
        @dataclass
        class FileParameters

        
    Creates the form for a "ProgramParameters" dataclass.
    """
    def __init__(self, config_class, program_class: Type[EMSoftProgram]):
        super().__init__()

        self.config_class = config_class
        self.program_class = program_class
        self.form_widgets = {}

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        for field_ in fields(config_class):
            if not field_.init:
                continue

            field_name = field_.name 
            field_type = field_.type

            if field_name.upper() == "FOIL":
                form = FoilForm()
                self.tabs.addTab(form, field_name.upper())
         
            elif field_name.upper() == "DEFECT":
                form = DefectForm()
                self.tabs.addTab(form, field_name.upper())

            elif is_dataclass(field_type):
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
            if program.update_input_name:
                program.copy_output_file(program.copy_output_from, program.name)
            elif program.copy_output_from:
                program.copy_output_file(program.copy_output_from)
            program.run()
        except Exception as e:
            print(f"[ERROR] Error while running program.")


    def _get_config(self):
        updated_config_data = {}

        for key, form in self.form_widgets.items():
            if isinstance(form, DataclassForm):
                form: DataclassForm
                updated_config_data[key] = form.get_instance()
            else:
                pass

        return self.config_class(**updated_config_data)
