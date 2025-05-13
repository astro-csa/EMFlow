import os
import shutil
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QScrollArea, QLabel, QPushButton, QFileDialog, QMessageBox
from gui.utils.vectors import create_vector_input, get_vector_string


class DefectType:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

DISLOCATION = DefectType(
    name="Dislocation",
    parameters=[
        ("id", float),
        ("jd", float),
        ("u", "vector"),
        ("bv", "vector"),
        ("zfrac", float)
    ]
)

STACKING_FAULTS = DefectType(
    name="Stacking Fault",
    parameters=[
        ("SFi", float),
        ("SFj", float),
        ("SFsep", float),
        ("SFplane", "vector"),
        ("SFlpu", "vector"),
        ("SFlpb", "vector"),
        ("SFtpu", "vector"),
        ("SFtpb", "vector")
    ]
)

DEFECT_TYPES = [DISLOCATION, STACKING_FAULTS]


class DefectForm(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.defects_by_type = {}

        self.select_file_button = QPushButton("Select Defect File")
        self.select_file_button.clicked.connect(self.select_existing_file)
        self.main_layout.addWidget(self.select_file_button)
        # Defect table
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: 1px solid gray;")
        self.scroll_area.setFixedHeight(300)

        self.defect_list_widget = QWidget()
        self.defect_list_layout = QVBoxLayout()
        self.defect_list_widget.setLayout(self.defect_list_layout)

        self.scroll_area.setWidget(self.defect_list_widget)

        self.empty_label = QLabel("No defects added.")
        self.empty_label.setStyleSheet("color: gray; font-style: italic;")
        self.defect_list_layout.addWidget(self.empty_label)

        self.main_layout.addWidget(self.scroll_area)

        # Defect selector
        selector_layout = QHBoxLayout()

        label = QLabel("Defect type:")
        self.combo_box = QComboBox()

        for defect in DEFECT_TYPES:
            self.combo_box.addItem(defect.name)

        selector_layout.addWidget(label)
        selector_layout.addWidget(self.combo_box)

        self.main_layout.addLayout(selector_layout)

        # Form container(Form, button)
        self.form_container = QWidget()
        self.param_form = QFormLayout()
        self.form_container.setLayout(self.param_form)
        self.main_layout.addWidget(self.form_container)

        self.combo_box.currentIndexChanged.connect(self.update_form)
        self.setLayout(self.main_layout)

        self.update_form()

    def update_form(self):
        try:
            self.main_layout.removeWidget(self.form_container)
            self.form_container.deleteLater()
        except Exception as e:
            print(f"[WARNING] Failed to remove previous defect form_container: {e}")

        self.form_container = QWidget()
        self.param_form = QFormLayout()
        self.form_container.setLayout(self.param_form)
        self.main_layout.addWidget(self.form_container)

        self.inputs = {}
        selected_name = self.combo_box.currentText()

        defect_type = next((d for d in DEFECT_TYPES if d.name == selected_name), None)
        if not defect_type:
            return

        for param_name, param_type in defect_type.parameters:
            if param_type == "vector":
                layout, input_widget = create_vector_input(param_name, 3)
                self.param_form.addRow(layout)
            else:
                input_widget = QLineEdit()
                self.param_form.addRow(param_name + ":", input_widget)
            self.inputs[param_name] = input_widget

        self.add_defect_button = QPushButton("Add defect.")
        self.add_defect_button.clicked.connect(self.add_defect)
        self.param_form.addWidget(self.add_defect_button)

        self.generate_button = QPushButton("Generate JSON")
        self.generate_button.clicked.connect(self.generate_json)
        self.param_form.addWidget(self.generate_button)


    def add_defect(self):
        defect_type_name = self.combo_box.currentText()
        parameters = {}

        defect_type = next((d for d in DEFECT_TYPES if d.name == defect_type_name), None)
        if not defect_type:
            return

        for param_name, param_type in defect_type.parameters:
            input_widget = self.inputs[param_name]

            if param_type == "vector":
                value = get_vector_string(input_widget)
            else:
                text = input_widget.text().strip()
                value = text if text else "0.0"

            parameters[param_name] = value

        self.defects_by_type.setdefault(defect_type_name, []).append(parameters)
        self.update_table()

    def update_table(self):
        # Clear layout
        while self.defect_list_layout.count():
            child = self.defect_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not any(self.defects_by_type.values()):
            label = QLabel("No defects added.")
            label.setStyleSheet("color: gray; font-style: italic;")
            self.defect_list_layout.addWidget(label)
            return

        for defect_type, defects_list in self.defects_by_type.items():
            title = QLabel(defect_type)
            title.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            self.defect_list_layout.addWidget(title)

            for index, defect in enumerate(defects_list):
                row_container = QWidget()
                row_layout = QHBoxLayout(row_container)

                for key, value in defect.items():
                    row_layout.addWidget(QLabel(f"{key}: {value}"))

                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(
                    lambda _, t=defect_type, i=index: self.delete_defect(t, i)
                )
                row_layout.addWidget(delete_button)

                self.defect_list_layout.addWidget(row_container)

    def delete_defect(self, defect_type, index):
        try:
            del self.defects_by_type[defect_type][index]
            if not self.defects_by_type[defect_type]:
                del self.defects_by_type[defect_type]
            self.update_table()
        except Exception as e:
            print(f"[ERROR] Couldn't delete defect: {e}")
    
    def select_existing_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Defect JSON", "", "JSON Files (*.json)")

        try:
            from gui.utils.config_context import ConfigContext
            target_dir = ConfigContext.get_data_path() / "EMFlow" / "temp" / "EMECCI"
            shutil.copy(path, os.path.join(target_dir, "EMdefect.json"))
            QMessageBox.information(self, "Success", "Defect file copied successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not copy file:\n{e}")
        return

    def generate_json(self):
        from gui.utils.config_context import ConfigContext
        path = ConfigContext.get_data_path() / "EMFlow/temp/EMECCI/EMdefect.json"
        lines = []
        lines.append("{")
        lines.append('    "DefectDescriptors": {')
        lines.append('        "foil": {')
        lines.append('            "foilfilename": "EMFlow/temp/EMECCI/EMfoil.json"')
        lines.append("        },")

        total_types = len(self.defects_by_type)
        for t_index, (defect_type, defects_list) in enumerate(self.defects_by_type.items()):
            lines.append(f'        "{defect_type}": [')
            for d_index, defect in enumerate(defects_list):
                lines.append("            {")
                keys = list(defect.items())
                for i, (key, val) in enumerate(keys):
                    comma = "," if i < len(keys) - 1 else ""
                    if "," in val:
                        lines.append(f'                "{key}": [ {val} ]{comma}')
                    else:
                        lines.append(f'                "{key}": {val}{comma}')
                lines.append("            }" + ("," if d_index < len(defects_list) - 1 else ""))
            lines.append("        ]" + ("," if t_index < total_types - 1 else ""))

        lines.append("    }")
        lines.append("}")

        try:
            with open(path, "w") as f:
                f.write("\n".join(lines))
            print(f"[INFO] JSON file saved to: {path}")
        except Exception as e:
            print(f"[ERROR] Failed to save JSON file: {e}")
