from ui.forms.common.experiment_form import ExperimentForm
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QStackedWidget, QVBoxLayout, QWidget
from emsoft.simulations.simulation_registry import SIMULATIONS


class SimulationSelector(QWidget):
    """
    A GUI widget that allows the user to select and configure a specific experiment
    (e.g., "ECCI" or "ECP") from a predefined list of simulations.

    This class creates a graphical interface with the following components:
        - A `QListWidget` containing the names of available experiments.
        - A `QStackedWidget` that displays the corresponding experiment form
          (parameters and configuration) based on the user's selection.
        - A console widget to display output or additional information.

    Attributes:
        - list_widget (QListWidget): Displays a list of experiment names (e.g., "ECCI", "ECP").
        - stacked_widget (QStackedWidget): Displays the configuration form for the selected experiment.
        - console (QWidget): A console widget for displaying experiment-related output or logs.
    """

    def __init__(self, console: QWidget):
        """
        Initializes the `SimulationSelector` widget.

        Args:
            console (QWidget): A QWidget that acts as a console or log output area,
                               which will be displayed alongside the experiment selection interface.
        """
        super().__init__()

        # Create a list widget to display the names of available simulations
        container = QWidget(self)
        v = QVBoxLayout(container)
        tittle = QLabel("Simulations", container)
        lst = QListWidget(container)

        v.addWidget(tittle)
        v.addWidget(lst)

        self.list_widget = lst

        # Create a stacked widget to hold the configuration forms for each experiment
        self.stacked_widget = QStackedWidget()

        # Set maximum and minimum widths for the list widget (to control its size in the GUI)
        container.setMaximumWidth(150)  # Maximum width of the list widget
        container.setMinimumWidth(100)  # Minimum width of the list widget

        # Store the console widget (provided as an argument)
        self.console = console

        # Set size constraints for the console widget
        self.console.setMinimumWidth(450)  # Minimum width of the console
        self.console.setMaximumWidth(850)  # Maximum width of the console

        # Populate the list widget with the names of the available simulations
        for name in SIMULATIONS.keys():
            self.list_widget.addItem(name)  # Add each simulation name to the list widget

        # Create and add experiment forms to the stacked widget for each simulation
        for experiment in SIMULATIONS.values():
            # Create an `ExperimentForm` for each experiment
            form = ExperimentForm(experiment)
            # Add the form to the stacked widget
            self.stacked_widget.addWidget(form)

        # Connect the `currentRowChanged` signal of the list widget to the `setCurrentIndex` slot
        # of the stacked widget. This ensures that the stacked widget switches to the correct
        # experiment form when the user selects a different experiment in the list.
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # Create a horizontal layout to organize the widgets
        layout = QHBoxLayout()
        layout.addWidget(container)  # Add the list widget to the layout (left side)
        layout.addWidget(self.stacked_widget)  # Add the stacked widget to the layout (middle)
        layout.addWidget(self.console)  # Add the console widget to the layout (right side)

        # Set the layout for the `SimulationSelector` widget
        self.setLayout(layout)
