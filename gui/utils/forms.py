from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit
from typing import List

def create_vector_input(label_text, size=3):
    layout = QHBoxLayout()
    label = QLabel(label_text)
    layout.addWidget(label)

    inputs = []
    for _ in range(size):
        input_box = QLineEdit()
        input_box.setFixedWidth(60)
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