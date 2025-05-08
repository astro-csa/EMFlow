from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit
from typing import List

def create_vector_boxes(size, default_value=None):
    if not default_value:
        default_value = ", ".join(["0.0"] * size)

    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)

    values = [v.strip() for v in default_value.split(",")]
    inputs = []

    for value in values:
        input_box = QLineEdit()
        input_box.setText(value)
        input_box.setMaximumWidth(50)
        layout.addWidget(input_box)
        inputs.append(input_box)
    
    return layout, inputs

def create_vector_input(label_text, size=3):
    layout = QHBoxLayout()
    label = QLabel(label_text)
    layout.addWidget(label)

    inputs = []
    for _ in range(size):
        input_box = QLineEdit()
        input_box.setMaximumWidth(35)
        layout.addWidget(input_box)
        inputs.append(input_box)

    return layout, inputs

def get_vector_string(vector_inputs: List[QLineEdit]):
    values = []
    for box in vector_inputs:
        text = box.text().strip()
        if text:
            values.append(text)
        else:
            values.append("0.0")
        
    return ", ".join(values)