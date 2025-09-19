from datetime import datetime

from ui.forms.common.program_form import ProgramForm
from ui.utils.config_context import ConfigContext
from ui.utils.defaults_manager import load_defaults
from ui.utils.tasks import SimulationTask
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from emsoft.common.emsoft_experiment import EMSoftExperiment


class ExperimentForm(QWidget):
    """
    A GUI widget for handling configuration and execution of an experiment.

    This class creates a graphical interface for an individual experiment. It allows users to:
        - View and configure the parameters for each program within the experiment.
        - Execute the entire sequence of programs as defined in the experiment.

    Attributes:
        - experiment (Experiment): The experiment object containing the sequence of steps (programs).
        - program_forms (list[ProgramForm]): A list of `ProgramForm` widgets, one for each program in the experiment.
        - run_button (QPushButton): A button to trigger the execution of the experiment.
    """

    def __init__(self, experiment: EMSoftExperiment):
        """
        Initializes the `ExperimentForm` widget.

        Args:
            experiment (Experiment): The experiment object containing the steps to be executed.
        """
        super().__init__()

        self.experiment = experiment  # Store the experiment object
        self.program_forms: list[ProgramForm] = []  # Initialize an empty list to store `ProgramForm` widgets

        # Create the main layout for the widget (vertical layout)
        main_layout = QVBoxLayout()

        # Create a horizontal layout to organize program forms
        program_layout = QHBoxLayout()

        # Iterate through the steps of the experiment and create a form for each program
        for step_name, program_class, config in experiment.steps:
            # Create a `ProgramForm` for the program's configuration
            form = ProgramForm(type(config), program_class)

            program_name = getattr(program_class, "name", step_name)
            user_defaults = load_defaults(
                experiment.name,
                program_name,
                type(config),
            )
            if user_defaults:
                form.load_config(user_defaults)

            # Create a group box to encapsulate the step
            group = QGroupBox(step_name)  # Use the step name as the title of the group box
            group_layout = QVBoxLayout()  # Create a vertical layout for the group box

            # Add the `ProgramForm` widget to the group box layout
            group_layout.addWidget(form)

            # Set the layout for the group box
            group.setLayout(group_layout)

            # Store the `ProgramForm` in the list of program forms
            self.program_forms.append(form)

            # Add the group box to the program layout
            program_layout.addWidget(group)

        # Add the program layout (horizontal) to the main layout (vertical)
        main_layout.addLayout(program_layout)

        # Create a button to run the simulation
        self.run_button = QPushButton("Run Simulation")
        # Connect the button's `clicked` signal to the `run_simulation` method
        self.run_button.clicked.connect(self.run_simulation)
        # Add the button to the main layout
        main_layout.addWidget(self.run_button)

        # Set the main layout for the widget
        self.setLayout(main_layout)

    def run_simulation(self):
        """
        Executes the experiment by running all steps (programs) in sequence.

        This method:
            1. Sets the current execution timestamp in the `ConfigContext`.
            2. Creates a `SimulationTask` with the program forms.
            3. Starts the task using a global thread pool for parallel execution.
        """
        # Generate a timestamp for the current execution (formatted as YYYY-MM-DD_HH-MM-SS)
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Set the execution timestamp in the `ConfigContext` for tracking purposes
        ConfigContext.set_execution_timestamp(now)

        # Create a simulation task, passing the list of program forms to handle the sequence
        task = SimulationTask(self.program_forms)
        # Start the task using the global thread pool (to offload execution to a separate thread)
        QThreadPool.globalInstance().start(task)
