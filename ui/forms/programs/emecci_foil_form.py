import os
import shutil
import sys

from ui.utils.vectors import create_vector_input
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FoilForm(QWidget):
    """
    A GUI form for defining and managing foil parameters.

    This form allows users to:
        - Enter parameters for foil simulation (e.g., vectors, scalars, and matrices).
        - Generate a JSON file for the foil descriptor.
        - Load an existing foil JSON file into the application.

    Attributes:
        - stack (QStackedWidget): A stacked widget to toggle between creating a new foil descriptor
          or using an existing file.
        - foilF_inputs, foilq_inputs (list[QLineEdit]): Input fields for 3-component vectors.
        - foilalP, foilalS, foilalR, foilz0 (QLineEdit): Input fields for scalar parameters.
        - foilelmo_inputs (list[list[QLineEdit]]): Input fields for a 6x6 matrix (foilelmo).
        - use_existing_checkbox (QCheckBox): Checkbox to toggle between using an existing file and creating a new one.
        - select_file_button (QPushButton): Button to load an existing foil JSON file.
        - button (QPushButton): Button to generate a new JSON file.
    """

    def __init__(self):
        super().__init__()

        # Main layout for the widget
        self.main_layout = QVBoxLayout()

        # Button to select an existing defect file
        self.select_file_button = QPushButton("Select Defect File")
        self.select_file_button.clicked.connect(self.select_existing_file)
        self.main_layout.addWidget(self.select_file_button)

        # Widget for creating a new foil descriptor
        self.foil_form_widget = QWidget()
        form_layout = QFormLayout(self.foil_form_widget)

        # Create 3-component vector inputs for "FoilF" and "Foilq"
        foilF_layout, self.foilF_inputs = create_vector_input("FoilF", 3)
        foilq_layout, self.foilq_inputs = create_vector_input("Foilq", 3)

        # Create 1-component scalar input fields
        self.foilalP = QLineEdit()  # Scalar input for FoilalP
        self.foilalS = QLineEdit()  # Scalar input for FoilalS
        self.foilalR = QLineEdit()  # Scalar input for FoilalR
        self.foilz0 = QLineEdit()  # Scalar input for Foilz0

        # Create 6x6 matrix input fields for "foilelmo"
        row_layouts = []
        self.foilelmo_inputs = []
        for i in range(6):  # 6 rows of the matrix
            row_layout, row_inputs = create_vector_input(f"Row {i + 1}", 6)
            row_layouts.append(row_layout)
            self.foilelmo_inputs.append(row_inputs)

        # Add fields to the form layout
        form_layout.addRow(foilF_layout)  # Add FoilF vector inputs
        form_layout.addRow(foilq_layout)  # Add Foilq vector inputs
        form_layout.addRow("FoilalP", self.foilalP)
        form_layout.addRow("FoilalS", self.foilalS)
        form_layout.addRow("FoilalR", self.foilalR)
        form_layout.addRow("Foilz0", self.foilz0)
        for row in row_layouts:  # Add each row of the matrix
            form_layout.addRow(row)

        # Add a button to generate the foil JSON file
        self.button = QPushButton("Generate json file")
        self.button.clicked.connect(self.generate_json)
        form_layout.addWidget(self.button)
        self.main_layout.addWidget(self.foil_form_widget)

        # Set the main layout for the widget
        self.setLayout(self.main_layout)

    def select_existing_file(self):
        """
        Opens a file dialog to select an existing foil JSON file.

        Copies the selected file to the target directory for use in the simulation.
        """
        path, _ = QFileDialog.getOpenFileName(self, "Select foil JSON", "", "JSON Files (*.json)")

        try:
            from ui.utils.config_context import ConfigContext

            target_dir = ConfigContext.get_data_path() / "EMFlow" / "temp" / "EMECCI"
            shutil.copy(path, os.path.join(target_dir, "EMfoil.json"))
            QMessageBox.information(self, "Success", "Foil file copied successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not copy file:\n{e}")
        return

    def generate_json(self):
        """
        Generates a JSON file for the foil descriptor based on the form input values.

        Opens a file dialog to save the generated JSON file.
        """
        try:
            # Retrieve values from the input fields
            foilF = ", ".join(str(float(box.text())) for box in self.foilF_inputs)
            foilq = ", ".join(str(float(box.text())) for box in self.foilq_inputs)
            foilalP = float(self.foilalP.text())
            foilalS = float(self.foilalS.text())
            foilalR = float(self.foilalR.text())
            foilz0 = float(self.foilz0.text())
            rows = {f"row{i + 1}": ", ".join(str(float(box.text())) for box in row) for i, row in enumerate(self.foilelmo_inputs)}

            # Generate the JSON string
            json_str = (
                "{\n"
                '  "FoilDescriptor": {\n'
                f'      "foilF": [ {foilF} ],\n'
                f'      "foilq": [ {foilq} ],\n'
                f'      "foilalP": {foilalP},\n'
                f'      "foilalS": {foilalS},\n'
                f'      "foilalR": {foilalR},\n'
                f'      "foilz0": {foilz0},\n'
                '      "foilelmo": {\n'
                f'          "row1": [ {rows["row1"]} ],\n'
                f'          "row2": [ {rows["row2"]} ],\n'
                f'          "row3": [ {rows["row3"]} ],\n'
                f'          "row4": [ {rows["row4"]} ],\n'
                f'          "row5": [ {rows["row5"]} ],\n'
                f'          "row6": [ {rows["row6"]} ]\n'
                "       }\n"
                "   }\n"
                "}"
            )

            # File dialog to save the JSON file
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Foil JSON", "EMfoil.json", "JSON Files (*.json)")

            if file_path:
                # Save the JSON file
                with open(file_path, "w") as f:
                    f.write(json_str)
                QMessageBox.information(self, "Éxito", "Archivo JSON generado correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el JSON:\n{e}")


if __name__ == "__main__":
    # Application entry point for testing the form
    app = QApplication(sys.argv)
    form = FoilForm()
    form.show()
    sys.exit(app.exec_())
