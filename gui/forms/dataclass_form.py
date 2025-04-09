from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFormLayout, QVBoxLayout, QMessageBox, QComboBox, QCheckBox
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from dataclasses import fields, is_dataclass

class DataclassForm(QWidget):
    def __init__(self, dataclass_type):
        super().__init__()

        assert is_dataclass(dataclass_type), "Must be a dataclass type"

        self.dataclass_type = dataclass_type
        self.instance = dataclass_type()
        self.inputs = {}

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        for f in fields(dataclass_type):
            if not f.init:
                continue
            default_value = getattr(self.instance, f.name)
            widget = self._build_widget(f, default_value)
            if f.metadata.get("visibility_controller"):
                if f.metadata.get("widget") == "combo":
                    widget.currentTextChanged.connect(self._update_visibility)

            form_layout.addRow(f.name, widget)
            self.inputs[f.name] = widget

        layout.addLayout(form_layout)
        self.setLayout(layout)

        for f in fields(self.dataclass_type):
            if f.metadata.get("visibility_controller"):
                self._update_visibility()
                break


    def get_instance(self):
        kwargs = {}
        for f in fields(self.dataclass_type):
            if not f.init:
                continue

            widget = self.inputs[f.name]
            if isinstance(widget, QLineEdit):
                text = widget.text()
                if f.type == int:
                    kwargs[f.name] = int(text)
                elif f.type == float:
                    kwargs[f.name] = float(text)
                else:
                    kwargs[f.name] = text
            elif isinstance(widget, QCheckBox):
                kwargs[f.name] = widget.isChecked()
            elif isinstance(widget, QComboBox):
                kwargs[f.name] = widget.currentText()
        return self.dataclass_type(**kwargs)
    
    def _build_widget(self, f, default_value):
        widget_type = f.metadata.get("widget")

        if widget_type == "combo":
            widget = QComboBox()
            options = f.metadata.get("options", [])
            widget.addItems(options)
        
        elif f.type == int:
            widget = QLineEdit()
            widget.setValidator(QIntValidator())
            widget.setText(str(default_value))
        elif f.type == float:
            widget = QLineEdit()
            widget.setValidator(QDoubleValidator())
            widget.setText(str(default_value))
        elif f.type == bool:
            widget = QCheckBox()
            widget.setChecked(default_value)
        else:
            widget = QLineEdit()
            widget.setText(str(default_value))
        return widget
    
    def _update_visibility(self):
        layout = self.layout()
        if not isinstance(layout, QVBoxLayout):
            return

        form_layout = layout.itemAt(0).layout()
        if not isinstance(form_layout, QFormLayout):
            return

        for f in fields(self.dataclass_type):
            depends_on = f.metadata.get("depends_on")
            expected = f.metadata.get("visible_if")

            if depends_on and expected:
                controller = self.inputs.get(depends_on)
                target_widget = self.inputs.get(f.name)

                if not isinstance(controller, QComboBox) or not target_widget:
                    continue

                current = controller.currentText()
                should_show = (current == expected)

                target_widget.setVisible(should_show)

                label = form_layout.labelForField(target_widget)
                if label:
                    label.setVisible(should_show)
