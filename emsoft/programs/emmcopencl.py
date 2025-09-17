from emsoft.common.emsoft_program import EMSoftProgram
from emsoft.parameters.emmcopencl import EMMCOpenCLParameters


class EMMCOpenCL(EMSoftProgram):
    """
    Class representing the `EMMCOpenCL` program, a specific implementation of an EMSoft program.

    This class inherits from the `EMSoftProgram` base class and provides specific configuration
    and behavior for the `EMMCOpenCL` program.

    Attributes:
        - name (str): The name of the program, which matches the executable name ("EMMCOpenCL").
        - config_class (type): The class used to represent the configuration for this program
          (in this case, `EMMCOpenCLParameters`).

    The class is designed to:
        - Provide a concrete implementation of the `EMSoftProgram` for the `EMMCOpenCL` executable.
        - Use a specific configuration dataclass (`EMMCOpenCLParameters`) to store and manage parameters.
    """

    # Name of the program, which corresponds to the executable file name
    name = "EMMCOpenCL"

    # The configuration dataclass to be used for this program
    config_class = EMMCOpenCLParameters

    def __init__(self, config):
        """
        Initializes the `EMMCOpenCL` program with a configuration.

        Args:
            config (object): An instance of the `EMMCOpenCLParameters` class containing
                             the configuration parameters for the program.
        """
        # Call the constructor of the parent class (`EMSoftProgram`) to initialize shared logic
        super().__init__(name=self.name, config=config)
