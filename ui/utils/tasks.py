import shutil

from ui.forms.common.program_form import ProgramForm
from ui.utils.config_context import ConfigContext
from PyQt5.QtCore import QRunnable


class SimulationTask(QRunnable):
    """
    A task for running a sequence of programs in the simulation.

    This class extends `QRunnable` to allow the simulation task to run in a separate thread,
    ensuring that the GUI remains responsive during execution.

    Attributes:
        - program_forms (list[ProgramForm]): A list of `ProgramForm` objects representing
          the steps (programs) in the simulation. Each form manages the configuration and
          execution for a specific program.

    Methods:
        - run(): Executes each program in the simulation sequence, then copies the output
          to a timestamped folder for archival purposes.
    """

    def __init__(self, program_forms: list[ProgramForm]):
        """
        Initializes the `SimulationTask`.

        Args:
            program_forms (list[ProgramForm]): A list of `ProgramForm` objects representing
                                               the steps in the simulation.
        """
        super().__init__()
        self.program_forms = program_forms  # Store the list of program forms

    def run(self):
        """
        Executes the simulation task.

        Workflow:
            1. Iterates through the list of `ProgramForm` objects and executes each program's `run_program` method.
            2. Archives the output by copying all temporary files to a timestamped folder for organized storage.
        """
        # Step 1: Execute each program in the sequence
        for program_form in self.program_forms:
            program_form: ProgramForm  # Ensure the item is treated as a `ProgramForm`
            program_form.run_program()  # Run the program associated with the form

        # Step 2: Retrieve the timestamped folder path
        timestamped_folder = ConfigContext.get_timestamped_folder()

        # Step 3: Retrieve the temporary directory path
        temp_config_path = ConfigContext.get_data_path() / "EMFlow" / "temp"

        # Step 4: Copy all files from the temporary directory to the timestamped folder
        # Use `shutil.copytree` with `dirs_exist_ok=True` to overwrite the directory if it already exists.
        shutil.copytree(str(temp_config_path), str(timestamped_folder), dirs_exist_ok=True)

        # Log the completion message with the path to the timestamped folder
        print(f"[INFO] Output copied to {timestamped_folder}")
