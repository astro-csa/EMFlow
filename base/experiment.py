from typing import List, Tuple, Type
from base.emsoft_program import EMSoftProgram

class Experiment:
    """
    Represents a high-level simulation composed of multiple EMSoft programs
    that must be executed in a specific sequence.

    Each step contains:
    - a name (e.g., "EMMCOpenCL")
    - a program class that inherits from EMSoftProgram
    - a configuration object (dataclass)

    This class allows grouped actions such as generating all configuration
    files or running all programs in sequence.
    """

    def __init__(self, name: str, steps: List[Tuple[str, Type[EMSoftProgram], object]]):
        """
        Initialize an Experiment.

        :param name: The name of the simulation (e.g. "ECCI")
        :param steps: A list of (step_name, program_class, config_instance) tuples
        """
        self.name = name
        self.steps = steps  # list of tuples (str, class, config instance)

    def generate_all_configs(self):
        """
        Calls generate_config() for all programs in order.
        """
        for step_name, program_class, config in self.steps:
            print(f"[INFO] Generating config for {step_name}")
            program = program_class(config=config)
            program.generate_config()

    def run_all(self):
        """
        (Optional) Run all programs in sequence.
        """
        for step_name, program_class, config in self.steps:
            print(f"[INFO] Running {step_name}")
            program = program_class(config=config)
            program.run()
