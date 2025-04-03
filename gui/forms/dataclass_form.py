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
            form_layout.addRow(f.name, widget)
            self.inputs[f.name] = widget

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def _build_widget(self, f, default_value):
        if f.type == int:
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
        elif f.name == "Notify":
            widget = QComboBox()
            widget.addItems(["Off", "On", "Slack"])
            index = widget.findText(default_value)
            if index >= 0:
                widget.setCurrentIndex(index)
        else:
            widget = QLineEdit()
            widget.setText(str(default_value))
        return widget

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