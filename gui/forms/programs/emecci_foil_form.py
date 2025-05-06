import sys
import os
import shutil
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFormLayout, QStackedWidget

from gui.utils.forms import create_vector_input

class FoilForm(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout()
        self.stack = QStackedWidget()

        self.foil_form_widget = QWidget()
        form_layout = QFormLayout(self.foil_form_widget)

        # 3-component vectors
        foilF_layout, self.foilF_inputs = create_vector_input("FoilF", 3)
        foilq_layout, self.foilq_inputs = create_vector_input("Foilq", 3)

        # 1-component scalars
        self.foilalP = QLineEdit()
        self.foilalS = QLineEdit()
        self.foilalR = QLineEdit()
        self.foilz0 = QLineEdit()

        # 6x6 matrix rows for foilelmo
        row_layouts = []
        self.foilelmo_inputs = []
        for i in range(6):
            row_layout, row_inputs = create_vector_input(f"Row {i+1}", 6)
            row_layouts.append(row_layout)
            self.foilelmo_inputs.append(row_inputs)

        # Add fields to form
        form_layout.addRow(foilF_layout)
        form_layout.addRow(foilq_layout)
        form_layout.addRow("FoilalP", self.foilalP)
        form_layout.addRow("FoilalS", self.foilalS)
        form_layout.addRow("FoilalR", self.foilalR)
        form_layout.addRow("Foilz0", self.foilz0)
        for row in row_layouts:
            form_layout.addRow(row)

        self.button = QPushButton("Generate json file")
        self.button.clicked.connect(self.generate_json)
        form_layout.addWidget(self.button)

        self.file_selector_widget = QWidget()
        selector_layout = QVBoxLayout(self.file_selector_widget)

        self.select_file_button = QPushButton("Select Foil File")
        self.select_file_button.clicked.connect(self.select_existing_file)
        self.copy_file_button = QPushButton("Copy json file")
        self.copy_file_button.clicked.connect(self.copy_json)
        selector_layout.addWidget(self.select_file_button)
        selector_layout.addWidget(self.copy_file_button)

        self.stack.addWidget(self.foil_form_widget)
        self.stack.addWidget(self.file_selector_widget)

        self.use_existing_checkbox = QCheckBox("Use existing Foil JSON")
        self.use_existing_checkbox.stateChanged.connect(self.toggle_foil_mode)
        layout.addRow(self.use_existing_checkbox)
        layout.addRow(self.stack)

        self.setLayout(layout)
    
    def toggle_foil_mode(self, state):
        if state == Qt.Checked:
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

    def select_existing_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Foil JSON", "", "JSON Files (*.json)")
        if path:
            self.existing_foil_path = path
            QMessageBox.information(self, "File Selected", f"Foil file selected:\n{path}")

    def generate_json(self):
        try:
            foilF = ", ".join(str(float(box.text())) for box in self.foilF_inputs)
            foilq = ", ".join(str(float(box.text())) for box in self.foilq_inputs)
            foilalP = float(self.foilalP.text())
            foilalS = float(self.foilalS.text())
            foilalR = float(self.foilalR.text())
            foilz0 = float(self.foilz0.text())
            rows = {
                f"row{i+1}": ", ".join(str(float(box.text())) for box in row)
                for i, row in enumerate(self.foilelmo_inputs)
            }

            json_str = (
                '{\n'
                '  "FoilDescriptor": {\n'
                f'      "foilF": [ {foilF} ],\n'
                f'      "foilq": [ {foilq} ],\n'
                f'      "foilalP": {foilalP},\n'
                f'      "foilalS": {foilalS},\n'
                f'      "foilalR": {foilalR},\n'
                f'      "foilz0": {foilz0},\n'
                '      "foilelmo": {\n'
                f'          "row1": [ {rows['row1']} ],\n'
                f'          "row2": [ {rows['row2']} ],\n'
                f'          "row3": [ {rows['row3']} ],\n'
                f'          "row4": [ {rows['row4']} ],\n'
                f'          "row5": [ {rows['row5']} ],\n'
                f'          "row6": [ {rows['row6']} ]\n'
                '       }\n'
                '   }\n'
                '}'
            )
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Foil JSON",
                "EMfoil.json",
                "JSON Files (*.json)"
            )

            if file_path:
                with open(file_path, "w") as f:
                    f.write(json_str)
                QMessageBox.information(self, "Éxito", "Archivo JSON generado correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el JSON:\n{e}")
    
    def copy_json(self):
        if not self.existing_foil_path:
                QMessageBox.warning(self, "Error", "No foil file selected.")
                return

        try:
            target_dir = os.path.join(os.getcwd(), "EMECCI")
            shutil.copy(self.existing_foil_path, os.path.join(target_dir, "EMfoil.json"))
            QMessageBox.information(self, "Success", "Foil file copied successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not copy file:\n{e}")
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FoilForm()
    form.show()
    sys.exit(app.exec_())