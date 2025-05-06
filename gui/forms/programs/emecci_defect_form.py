from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QScrollArea, QLabel, QPushButton
from gui.utils.forms import create_vector_input, get_vector_string

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

        # Form container(Form, button, spacer)
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

        # Form
        self.form_container = QWidget()
        self.param_form = QFormLayout()
        self.form_container.setLayout(self.param_form)
        self.main_layout.addWidget(self.form_container)

        self.inputs = {}

        selected_name = self.combo_box.currentText()

        defect_type = None
        for defect in DEFECT_TYPES:
            if defect.name == selected_name:
                defect_type = defect
                break

        if defect_type is None:
            return

        for param_name, param_type in defect_type.parameters:
            if param_type == "vector":
                layout, input_widget = create_vector_input(param_name, 3)
                self.param_form.addRow(layout)
            else:
                input_widget = QLineEdit()
                self.param_form.addRow(param_name + ":", input_widget)
            self.inputs[param_name] = input_widget
        
        # Button
        self.add_defect_button = QPushButton("Add defect.")
        self.add_defect_button.pressed.connect(self.add_defect)
        self.param_form.addWidget(self.add_defect_button)
        
    def add_defect(self):
        defect_type_name = self.combo_box.currentText()
        parameters = {}

        defect_type = None
        for defect in DEFECT_TYPES:
            if defect.name == defect_type_name:
                defect_type = defect
                break

        if defect_type is None:
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
       # Delete the whole layout
        while self.defect_list_layout.count():
            child = self.defect_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # If there are not defects
        if not any(self.defects_by_type.values()):
            label = QLabel("No defects added.")
            label.setStyleSheet("color: gray; font-style: italic;")
            self.defect_list_layout.addWidget(label)
            return


        # Draw
        for defect_type, defects_list in self.defects_by_type.items():
            title = QLabel(defect_type)
            title.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            self.defect_list_layout.addWidget(title)

            for index, defect in enumerate(defects_list):
                row_container = QWidget()
                row_layout = QHBoxLayout(row_container)

                for key, value in defect.items():
                    label = QLabel(f"{key}: {value}")
                    row_layout.addWidget(label)

                # Botón Edit
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda _, t=defect_type, i=index: self.edit_defect(t, i))

                # Botón Delete
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, t=defect_type, i=index: self.delete_defect(t, i))

                row_layout.addWidget(edit_button)
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

    def edit_defect(self, defect_type, index):
        self.editing_type = defect_type
        self.editing_index = index

        defect_data = self.defects_by_type[defect_type][index]

        # Cargar datos en los widgets
        for param_name, widget in self.inputs.items():
            value = defect_data.get(param_name, "")
            if isinstance(widget, QLineEdit):
                widget.setText(value)
            elif isinstance(widget, list):  # vector
                parts = value.split(",")
                for i, part in enumerate(parts):
                    if i < len(widget):
                        widget[i].setText(part.strip())

        # Cambiar el botón a "Update defect"
        self.add_defect_button.setText("Update defect")

        # Desconectar lo que estuviera conectado antes
        try:
            self.add_defect_button.clicked.disconnect(self.add_defect)
        except TypeError:
            pass

        try:
            self.add_defect_button.clicked.disconnect(self.update_defect)
        except TypeError:
            pass

        # Conectar sólo a update_defect
        self.add_defect_button.clicked.connect(self.update_defect)


    def update_defect(self):
        defect_type = self.editing_type
        index = self.editing_index
        updated_params = {}

        for param_name, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                updated_params[param_name] = widget.text()
            elif isinstance(widget, list):
                updated_params[param_name] = get_vector_string(widget)

        self.defects_by_type[defect_type][index] = updated_params

        # Restaurar el botón
        self.add_defect_button.setText("Add defect")

        try:
            self.add_defect_button.clicked.disconnect(self.update_defect)
        except TypeError:
            pass

        try:
            self.add_defect_button.clicked.disconnect(self.add_defect)
        except TypeError:
            pass

        self.add_defect_button.clicked.connect(self.add_defect)

        self.editing_type = None
        self.editing_index = None

        self.update_table()


