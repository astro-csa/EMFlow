from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit

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
