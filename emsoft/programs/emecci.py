from emsoft.common.emsoft_program import EMSoftProgram
from emsoft.parameters.emecci import EMECCIParameters
from emsoft.programs.emecp import EMECP


class EMECCI(EMSoftProgram):
    """
    Class representing the `EMECCI` program, a specific implementation of an EMSoft program.

    This class is tailored for the `EMECCI` executable. It inherits from the `EMSoftProgram`
    base class and defines additional attributes to handle configuration and dependencies
    specific to the `EMECCI` program.

    Attributes:
        - name (str): The name of the program, which corresponds to the executable name ("EMECCI").
        - config_class (type): The configuration dataclass for the program (`EMECCIParameters`).
        - copy_output_from (type): Specifies the program from which the output file is copied
          as input for this program (in this case, `EMECP`).

    Purpose:
        - Integrates `EMECCI` into workflows by managing its configuration, execution,
          and dependencies on the `EMECP` program.
    """

    # Name of the program, corresponding to the executable file name
    name = "EMECCI"

    # Configuration dataclass used to manage parameters for this program
    config_class = EMECCIParameters

    def __init__(self, config):
        """
        Initializes the `EMECCI` program with its configuration.

        Args:
            config (object): An instance of the `EMECCIParameters` dataclass containing
                             configuration parameters for the program.
        """
        # Call the parent class constructor to initialize shared attributes and logic
        super().__init__(name=self.name, config=config)

        # Specify that this program's input depends on the output of the `EMECP` program
        self.copy_output_from = EMECP
