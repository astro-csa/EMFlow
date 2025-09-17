from emsoft.common.emsoft_program import EMSoftProgram
from emsoft.parameters.emecp import EMECPParameters
from emsoft.programs.emecpmaster import EMECPmaster


class EMECP(EMSoftProgram):
    """
    Class representing the `EMECP` program, a specific implementation of an EMSoft program.

    This class is tailored to the `EMECP` executable, inheriting behavior and functionality
    from the `EMSoftProgram` base class while providing additional attributes for
    dependencies and configurations specific to `EMECP`.

    Attributes:
        - name (str): The name of the program, corresponding to the executable ("EMECP").
        - config_class (type): The configuration dataclass for the program (`EMECPParameters`).
        - copy_output_from (type): Specifies the program from which the output file is copied
          as input for this program (in this case, `EMECPmaster`).

    Purpose:
        - Integrates `EMECP` into workflows by managing dependencies, configurations,
          and execution of the program.
        - Ensures that the program's input depends on the output of `EMECPmaster`.
    """

    # Name of the program, corresponding to the executable file name
    name = "EMECP"

    # Configuration dataclass used to define parameters for this program
    config_class = EMECPParameters

    def __init__(self, config):
        """
        Initializes the `EMECP` program with its specific configuration.

        Args:
            config (object): An instance of the `EMECPParameters` dataclass containing
                             configuration parameters for the program.
        """
        # Call the parent class constructor to initialize shared attributes and logic
        super().__init__(name=self.name, config=config)

        # Specify that this program's input depends on the output of the `EMECPmaster` program
        self.copy_output_from = EMECPmaster
