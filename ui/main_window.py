import sys

from ui.dialogs.default_values_dialog import DefaultValuesDialog
from ui.layout.simulation_selector import SimulationSelector
from ui.menu_bar import MenuBar
from ui.utils.config_context import ConfigContext
from ui.utils.config_manager import get_data_path
from ui.utils.console_redirector import EmittingStream
from ui.widgets.console_widget import ConsoleWidget
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """
    Main window class for the EMFlow application.

    This class defines the main GUI layout and integrates the simulation selector,
    console widget, and configuration context. It acts as the central window for
    the application, allowing users to select and configure simulations.

    Attributes:
        - main_layout (QVBoxLayout): The main vertical layout containing the simulation selector.
        - widget (SimulationSelector): The simulation selector widget for experiment configuration.
    """

    def __init__(self):
        """
        Initializes the main window of the EMFlow application.

        Args:
            console_widget (ConsoleWidget): A console widget for displaying logs and output.
        """
        super().__init__()

        # Set the window title
        self.setWindowTitle("EMFlow - Configuration Generator")

        # Create the application menu bar
        self.menu_bar = MenuBar(
            self,
            on_modify_defaults=self.modify_default_values,
            on_restore_defaults=self.restore_original_values,
        )
        self.setMenuBar(self.menu_bar)

        # Set the data path using the configuration manager
        ConfigContext.set_data_path(get_data_path())

        # Create the console widget to display logs and output
        self.console_widget = ConsoleWidget()

        # Create an emitting stream to redirect stdout and stderr to the console widget
        self.stream = EmittingStream()
        self.stream.text_written.connect(self.console_widget.append)  # Connect the stream output to the console widget

        # Redirect stdout and stderr to the emitting stream
        sys.stdout = self.stream
        sys.stderr = self.stream

        # Create the main vertical layout
        self.main_layout = QVBoxLayout()

        # Add the simulation selector widget, passing the console widget to it
        self.widget = SimulationSelector(self.console_widget)
        self.main_layout.addWidget(self.widget)

        # Set up the central widget with the main layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def modify_default_values(self):
        experiment = self.widget.current_experiment()
        if experiment is None:
            QMessageBox.warning(
                self,
                "No Experiment Selected",
                "Select an experiment before modifying default values.",
            )
            return

        dialog = DefaultValuesDialog(experiment, self)
        dialog.exec_()

    def restore_original_values(self):
        QMessageBox.information(
            self,
            "Restore Original Values",
            "This action is not implemented yet.",
        )
