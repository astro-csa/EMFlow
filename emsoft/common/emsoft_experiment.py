from emsoft.common.emsoft_program import EMSoftProgram


class EMSoftExperiment:
    """
    Represents a high-level simulation consisting of multiple EMSoft programs
    that need to be executed in a specific sequence. Each step of the simulation
    corresponds to a program with its own configuration.

    The purpose of this class is to organize and streamline the process of:
    - Generating all necessary configuration files for each program in the experiment.
    - Running each program in the correct order.

    Attributes:
        - name (str): The name of the experiment (e.g., "ECCI").
        - steps (list[tuple[str, type[EMSoftProgram], object]]): A list of steps,
          where each step is a tuple containing:
            - step_name (str): The name of the step (e.g., "EMMCOpenCL").
            - program_class (type[EMSoftProgram]): A class inheriting from `EMSoftProgram`.
            - config_instance (object): A dataclass instance containing the configuration
              for the specific program.
    """

    def __init__(self, name: str, steps: list[tuple[str, type[EMSoftProgram], object]]):
        """
        Initializes an Experiment object with a name and a sequence of steps.

        Args:
            name (str): The name of the simulation (e.g., "ECCI").
            steps (list[tuple[str, type[EMSoftProgram], object]]):
                A list of tuples, where each tuple contains:
                - step_name (str): The name of the step.
                - program_class (type[EMSoftProgram]): A subclass of `EMSoftProgram`
                  representing the program to be executed in this step.
                - config_instance (object): An instance of a configuration dataclass
                  that provides the parameters for the program.

        Example:
            steps = [
                ("Step1", EMMCOpenCL, ConfigClass1()),
                ("Step2", EMEBSD, ConfigClass2()),
            ]
        """
        self.name = name  # Name of the experiment
        self.steps = steps  # List of steps for the experiment

    def generate_all_configs(self):
        """
        Generates configuration files for all steps in the experiment.

        This method iterates through the steps defined in the experiment, instantiates
        each program using its associated class and configuration, and calls the
        `generate_config()` method to produce the required configuration files.

        Example Output:
            [INFO] Generating config for Step1
            [INFO] Generating config for Step2

        Raises:
            RuntimeError: If a step's program class or its configuration is invalid.
        """
        for step_name, program_class, config in self.steps:
            print(f"[INFO] Generating config for {step_name}")
            # Instantiate the program with the provided configuration
            program = program_class(config=config)
            # Call the program's method to generate its configuration files
            program.generate_config()

    def run_all(self):
        """
        Executes all programs in the experiment in sequential order.

        This method iterates through the steps in the experiment, instantiates
        each program using its associated class and configuration, and calls the
        `run()` method to execute it.

        Example Output:
            [INFO] Running Step1
            [INFO] Running Step2

        Note:
            - This method assumes that the programs are designed to be executed
              sequentially and that dependencies between steps (e.g., output files)
              are handled correctly.

        Raises:
            RuntimeError: If a step's program fails to execute or if any required
                          dependencies are missing.
        """
        for step_name, program_class, config in self.steps:
            print(f"[INFO] Running {step_name}")
            # Instantiate the program with the provided configuration
            program = program_class(config=config)
            # Call the program's run method to execute it
            program.run()
