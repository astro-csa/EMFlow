from emsoft.common.emsoft_program import EMSoftProgram
from emsoft.parameters.emecpmaster import EMECPmasterParameters
from emsoft.programs.emmcopencl import EMMCOpenCL


class EMECPmaster(EMSoftProgram):
    """
    Class representing the `EMECPmaster` program, a specific implementation of an EMSoft program.

    This class is tailored for the `EMECPmaster` executable, inheriting from the `EMSoftProgram` base class and
    providing additional attributes and behaviors specific to `EMECPmaster`.

    Attributes:
        - name (str): The name of the program, corresponding to the executable name ("EMECPmaster").
        - config_class (type): The configuration dataclass for the program (`EMECPmasterParameters`).
        - copy_output_from (type): Specifies the program from which the output file is copied
          (in this case, `EMMCOpenCL`).
        - update_input_name (bool): A flag indicating whether the input file name needs to be updated
          during the program's configuration or execution.

    This class is designed to:
        - Use the configuration dataclass `EMECPmasterParameters` to manage program-specific parameters.
        - Define dependencies on the output of `EMMCOpenCL` as an input for this program.
        - Provide shared functionality for configuration generation and execution by extending `EMSoftProgram`.
    """

    # Name of the program, corresponding to the executable file name
    name = "EMECPmaster"

    # Dataclass used to represent the configuration parameters for this program
    config_class = EMECPmasterParameters

    def __init__(self, config):
        """
        Initializes the `EMECPmaster` program with a configuration.

        Args:
            config (object): An instance of the `EMECPmasterParameters` dataclass containing
                             the configuration parameters for the program.
        """
        # Call the parent class constructor to initialize shared attributes and functionality
        super().__init__(name=self.name, config=config)

        # Specify that this program's input depends on the output of the `EMMCOpenCL` program
        self.copy_output_from = EMMCOpenCL

        # Set a flag indicating that the input file name needs to be updated dynamically
        self.update_input_name = True
