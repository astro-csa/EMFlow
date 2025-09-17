from dataclasses import MISSING, Field, fields

from ui.utils.vectors import create_vector_boxes, get_vector_string
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QCheckBox, QComboBox, QFormLayout, QLineEdit, QVBoxLayout, QWidget


class DataclassForm(QWidget):
    """
    A GUI widget for dynamically creating a form based on a given dataclass structure.

    This class maps the fields of a `dataclass` to corresponding input widgets (e.g.,
    text fields, combo boxes, checkboxes) and handles the logic for retrieving user input
    as an updated instance of the dataclass.

    Attributes:
        - dataclass_type: The dataclass type that defines the structure of the form.
        - instance: An instance of the dataclass (initialized with default values).
        - inputs (dict): A dictionary mapping field names to their corresponding input widgets.
        - vector_inputs (dict): A dictionary mapping vector field names to their input widgets.
    """

    def __init__(self, dataclass_type):
        """
        Initializes the `DataclassForm` widget.

        Args:
            dataclass_type: The dataclass type that defines the form structure.
        """
        super().__init__()

        self.dataclass_type = dataclass_type  # Store the dataclass type
        self.instance = dataclass_type()  # Create an instance of the dataclass
        self.inputs = {}  # Dictionary to store input widgets for each field
        self.vector_inputs = {}  # Dictionary to store input widgets for vector fields

        # Create the main layout for the widget
        layout = QVBoxLayout()
        # Create a form layout to organize the input fields
        form_layout = QFormLayout()

        # Iterate over each field in the dataclass
        for f in fields(dataclass_type):
            if not f.init:  # Skip fields that are not meant to be initialized
                continue

            # Determine the default value for the field
            if f.default is not MISSING:
                default_value = f.default
            elif f.default_factory is not MISSING:
                default_value = f.default_factory()
            else:
                default_value = None

            # Build the corresponding input widget for the field
            widget = self._build_widget(f, default_value)

            # Handle visibility controllers for combo boxes
            if f.metadata.get("visibility_controller"):
                if f.metadata.get("widget") == "combo":
                    widget: QComboBox
                    widget.currentTextChanged.connect(self._update_visibility)

            # Add the widget to the form layout and store it in the `inputs` dictionary
            form_layout.addRow(f.name, widget)
            self.inputs[f.name] = widget

        # Add the form layout to the main layout
        layout.addLayout(form_layout)
        # Set the main layout for the widget
        self.setLayout(layout)

        # Update visibility for fields based on visibility controllers
        for f in fields(self.dataclass_type):
            if f.metadata.get("visibility_controller"):
                self._update_visibility()
                break

    def get_instance(self):
        """
        Retrieves the current state of the form as an instance of the dataclass.

        Returns:
            An instance of the dataclass with updated values from the form.
        """
        kwargs = {}  # Dictionary to store updated parameter values

        # Iterate through each field
        for f in fields(self.dataclass_type):
            if not f.init:  # Skip fields that are not meant to be initialized
                continue

            widget = self.inputs[f.name]  # Get the corresponding input widget
            widget_type = f.metadata.get("widget")  # Get the widget type from metadata

            if widget_type == "vector":
                # Handle vector inputs
                vector_inputs = self.vector_inputs.get(f.name, [])
                kwargs[f.name] = get_vector_string(vector_inputs)

            elif isinstance(widget, QLineEdit):
                # Handle text inputs
                text = widget.text()
                if f.type is int:
                    kwargs[f.name] = int(text)
                elif f.type is float:
                    kwargs[f.name] = float(text)
                else:
                    kwargs[f.name] = text

            elif isinstance(widget, QCheckBox):
                # Handle checkbox inputs
                kwargs[f.name] = widget.isChecked()

            elif isinstance(widget, QComboBox):
                # Handle combo box inputs
                kwargs[f.name] = widget.currentText()

        # Create and return a new instance of the dataclass with updated values
        return self.dataclass_type(**kwargs)

    """
    def select_existing_file(self, program_name):
        path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "(*.nml)")

        try:
            from gui.utils.config_context import ConfigContext
            target_dir = ConfigContext.get_data_path() / "EMFlow" / "temp" / program_name
            shutil.copy(path, os.path.join(target_dir, ))
            QMessageBox.information(self, "Success", "Defect file copied successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not copy file:\n{e}")
        return
    """

    def _build_widget(self, f: Field, default_value) -> QWidget:
        """
        Creates an input widget for a given dataclass field.

        Args:
            f (Field): The dataclass field definition.
            default_value: The default value for the field.

        Returns:
            QWidget: The created input widget.
        """
        widget_type = f.metadata.get("widget")  # Retrieve the widget type from metadata

        if widget_type == "combo":
            # Create a combo box for selection
            widget = QComboBox()
            options = f.metadata.get("options", [])  # Retrieve options from metadata
            widget.addItems(options)
            if str(default_value) in options:
                widget.setCurrentText(str(default_value))
            else:
                widget.setCurrentIndex(0)

        elif widget_type == "vector":
            # Create vector input fields
            size = f.metadata.get("size", 3)  # Default size is 3 (e.g., x, y, z)
            default_value = f.metadata.get("default_value", None)  # Default vector value
            layout, vector_inputs = create_vector_boxes(size, default_value)
            container = QWidget()  # Create a container widget for the vector inputs
            container.setLayout(layout)
            self.vector_inputs[f.name] = vector_inputs  # Store the vector inputs
            return container  # Return the container widget

        elif f.type is int:
            # Create a line edit with integer validation
            widget = QLineEdit()
            widget.setValidator(QIntValidator())
            widget.setText(str(default_value))

        elif f.type is float:
            # Create a line edit with float validation
            widget = QLineEdit()
            widget.setValidator(QDoubleValidator())
            widget.setText(str(default_value))

        elif f.type is bool:
            # Create a checkbox for boolean fields
            widget = QCheckBox()
            widget.setChecked(default_value)

        else:
            # Default to a line edit for all other field types
            widget = QLineEdit()
            widget.setText(str(default_value))

        return widget  # Return the created widget

    def _update_visibility(self):
        """
        Updates the visibility of fields based on the values of their dependencies.

        Fields can have metadata specifying their visibility conditions, such as:
            - "depends_on": The name of the controlling field.
            - "visible_if": The expected value of the controlling field.

        This method checks these conditions and toggles the visibility of the dependent fields.
        """
        layout = self.layout()
        if not isinstance(layout, QVBoxLayout):
            return

        form_layout = layout.itemAt(0).layout()
        if not isinstance(form_layout, QFormLayout):
            return

        # Iterate through each field in the dataclass
        for f in fields(self.dataclass_type):
            depends_on = f.metadata.get("depends_on")  # Get the controlling field
            expected = f.metadata.get("visible_if")  # Get the expected value

            if depends_on and expected:
                controller = self.inputs.get(depends_on)  # Get the controlling widget
                target_widget: QWidget = self.inputs.get(f.name)  # Get the target widget

                if not isinstance(controller, QComboBox) or not target_widget:
                    continue

                current = controller.currentText()  # Current value of the controlling widget
                should_show = current == expected  # Check if the value matches the expected condition

                target_widget.setVisible(should_show)  # Toggle visibility of the target widget

                # Toggle visibility of the label associated with the target widget
                label = form_layout.labelForField(target_widget)
                if label:
                    label.setVisible(should_show)
