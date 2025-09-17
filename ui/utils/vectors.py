from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


def create_vector_boxes(size, default_value=None):
    """
    Creates a horizontal layout containing a specified number of input boxes for vector components.

    Args:
        size (int): The number of input boxes to create (i.e., the vector size).
        default_value (str | None): A comma-separated string of default values for the inputs (e.g., "1.0, 0.0, 0.0").
                                    If `None`, the default values are initialized to "0.0" for all components.

    Returns:
        tuple: A tuple containing:
            - QHBoxLayout: The horizontal layout with the input boxes.
            - list[QLineEdit]: A list of input box widgets for the vector components.
    """
    if not default_value:
        # Initialize default values to "0.0" for all components if no default is provided
        default_value = ",".join(["0.0"] * size)

    # Create a horizontal layout with no margins
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)

    # Parse the default value into individual components
    values = [v.strip() for v in default_value.split(",")]
    inputs = []

    # Create a QLineEdit for each vector component and add it to the layout
    for value in values:
        input_box = QLineEdit()
        input_box.setText(value)  # Set the default value
        input_box.setMaximumWidth(50)  # Limit the width of the input box
        layout.addWidget(input_box)  # Add the input box to the layout
        inputs.append(input_box)  # Keep track of the input box in a list

    return layout, inputs  # Return the layout and the list of input boxes


def create_vector_input(label_text, size=3):
    """
    Creates a labeled input layout for a vector.

    Args:
        label_text (str): The label to display next to the vector input boxes.
        size (int): The number of input boxes to create for the vector (default is 3 for a 3D vector).

    Returns:
        tuple: A tuple containing:
            - QHBoxLayout: The horizontal layout with the label and the input boxes.
            - list[QLineEdit]: A list of input box widgets for the vector components.
    """
    # Create a horizontal layout
    layout = QHBoxLayout()

    # Add a label to the layout
    label = QLabel(label_text)
    layout.addWidget(label)

    # Create input boxes for the vector components
    inputs = []
    for _ in range(size):
        input_box = QLineEdit()
        input_box.setMaximumWidth(35)  # Set a smaller width for compactness
        layout.addWidget(input_box)  # Add the input box to the layout
        inputs.append(input_box)  # Add the input box to the list of inputs

    return layout, inputs  # Return the layout and the list of input boxes


def get_vector_string(vector_inputs: list[QLineEdit]):
    """
    Retrieves the values from a list of QLineEdit input boxes and formats them into a comma-separated string.

    Args:
        vector_inputs (list[QLineEdit]): A list of input boxes representing vector components.

    Returns:
        str: A comma-separated string of vector components (e.g., "1.0,0.0,2.5").
             If a box is empty, its value is replaced with "0.0".
    """
    values = []

    # Iterate through each QLineEdit box in the vector
    for box in vector_inputs:
        text = box.text().strip()  # Get and trim the text from the input box
        if text:
            values.append(text)  # If the box has text, use it
        else:
            values.append("0.0")  # If the box is empty, default to "0.0"

    # Join the values into a comma-separated string
    return ",".join(values)
