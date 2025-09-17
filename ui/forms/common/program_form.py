from dataclasses import fields, is_dataclass

from ui.forms.common.dataclass_form import DataclassForm
from ui.forms.programs.emecci_defect_form import DefectForm
from ui.forms.programs.emecci_foil_form import FoilForm
from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout, QWidget

from emsoft.common.emsoft_program import EMSoftProgram


class ProgramForm(QWidget):
    """
    A GUI widget for handling the configuration and execution of a program's parameters.

    This class dynamically generates input forms for the parameters of a given program, based on the structure
    of its associated dataclass. It supports different types of nested dataclass structures, as well as custom
    forms for special parameter types (e.g., "FOIL" and "DEFECT").

    Attributes:
        - config_class: The dataclass that defines the program's parameters.
        - program_class (type[EMSoftProgram]): The class representing the specific program to be configured.
        - form_widgets (dict): A dictionary that maps parameter names to their corresponding input forms.
        - tabs (QTabWidget): A tabbed widget to organize parameter input forms for various sections of the program.
        - generate_button (QPushButton): A button to trigger the generation of the program's configuration file.
    """

    def __init__(self, config_class, program_class: type[EMSoftProgram]):
        """
        Initializes the `ProgramForm` widget.

        Args:
            config_class: The dataclass that defines the structure and default values for the program's parameters.
            program_class (type[EMSoftProgram]): The class representing the program to be configured.
        """
        super().__init__()

        self.config_class = config_class  # Store the configuration dataclass
        self.program_class = program_class  # Store the program class
        self.form_widgets = {}  # Initialize an empty dictionary to store parameter input forms

        # Create the main layout for the widget
        layout = QVBoxLayout()

        # Create a tabbed widget to organize parameter input forms for different sections
        self.tabs = QTabWidget()

        # Iterate through the fields of the configuration dataclass
        for field_ in fields(config_class):
            if not field_.init:
                # Skip fields that are not initialized (e.g., fields with `init=False`)
                continue

            field_name = field_.name  # Name of the field
            field_type = field_.type  # Type of the field

            # Check if the field corresponds to special forms (e.g., "FOIL" or "DEFECT")
            if field_name.upper() == "FOIL":
                # Create a custom form for FOIL parameters
                form = FoilForm()
                self.tabs.addTab(form, field_name.upper())

            elif field_name.upper() == "DEFECT":
                # Create a custom form for DEFECT parameters
                form = DefectForm()
                self.tabs.addTab(form, field_name.upper())

            elif is_dataclass(field_type):
                # If the field type is a nested dataclass, create a generic `DataclassForm`
                form = DataclassForm(field_type)
                # Store the form in the `form_widgets` dictionary for later use
                self.form_widgets[field_name] = form
                # Add the form to the tabs widget
                self.tabs.addTab(form, field_name.upper())

        # Add the tabs widget to the main layout
        layout.addWidget(self.tabs)

        # Create a button to generate the program's configuration file
        self.generate_button = QPushButton("Generate Config")
        # Connect the button's click event to the `generate_config` method
        self.generate_button.clicked.connect(self.generate_config)
        # Add the button to the main layout
        layout.addWidget(self.generate_button)

        # Set the main layout for the widget
        self.setLayout(layout)

    def generate_config(self):
        """
        Generates the configuration file for the program based on the user input.

        This method:
            1. Collects the updated parameter values from the input forms.
            2. Instantiates the program with the updated configuration.
            3. Calls the program's `generate_config` method to create the configuration file.
        """
        try:
            # Retrieve the updated configuration from the input forms
            config = self._get_config()
            # Instantiate the program class with the updated configuration
            program = self.program_class(config=config)
            # Generate the configuration file for the program
            program.generate_config()
        except Exception as e:
            print(f"[ERROR] Failed to generate config: {e}")  # Log any errors

    def run_program(self):
        """
        Executes the program using the current configuration.

        This method:
            1. Collects the updated parameter values from the input forms.
            2. Instantiates the program with the updated configuration.
            3. Handles input dependencies (e.g., copying output files from other programs).
            4. Calls the program's `run` method to execute it.
        """
        try:
            # Retrieve the updated configuration from the input forms
            config = self._get_config()
            # Instantiate the program class with the updated configuration
            program = self.program_class(config=config)

            # Handle input dependencies, if applicable
            if program.update_input_name:
                # If input names need to be updated, copy and rename the output file
                program.copy_output_file(program.copy_output_from, program.name)
            elif program.copy_output_from:
                # Otherwise, simply copy the output file from the dependency
                program.copy_output_file(program.copy_output_from)

            # Execute the program
            program.run()
        except Exception as e:
            print(f"[ERROR] Error while running program: {e}")  # Log any errors

    def _get_config(self):
        """
        Collects the updated configuration data from the input forms.

        Returns:
            An instance of the configuration dataclass (`config_class`) with the updated values.
        """
        updated_config_data = {}

        # Iterate through the forms stored in `form_widgets`
        for key, form in self.form_widgets.items():
            if isinstance(form, DataclassForm):
                # If the form is a `DataclassForm`, retrieve the updated instance
                form: DataclassForm
                updated_config_data[key] = form.get_instance()
            else:
                # Handle other types of forms, if needed (currently ignored)
                pass

        # Create and return a new instance of the configuration dataclass with the updated values
        return self.config_class(**updated_config_data)
