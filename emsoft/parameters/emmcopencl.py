from dataclasses import dataclass, field

from emsoft.common.emsoft_config import EMSoftConfig


@dataclass
class EMMCOpenCLParameters(EMSoftConfig):
    """
    Dataclass representing the configuration parameters for the EMMCOpenCL program.

    Contains nested dataclass `NML`, which stores parameters specific to the `.nml` configuration file.
    The parameters include simulation modes, crystal structure files, computation grid sizes, and other
    program-specific settings. Metadata is provided for UI widgets, conditional visibility of parameters,
    and validation dependencies.

    Attributes:
        - nml (NML): Nested dataclass storing `.nml` configuration parameters.
    """

    @dataclass
    class NML:
        """
        Nested dataclass representing the `.nml` configuration parameters for the EMMCOpenCL program.

        Attributes:
            mode (str): The mode of the simulation, with options like "bse1", "full", and "Ivol".
                        Metadata is provided for GUI widget rendering and visibility control.

            xtalname (str): The name of the crystal structure file (e.g., "GaN.xtal").
            numsx (int): Number of grid points in the x-direction for computations.

            sig, omega (float): Parameters for the "full" simulation mode. These fields are visible only
                                when `mode == "full"`.

            sigstart, sigend, sigstep (float): Parameters for the "bse1" simulation mode. These fields are
                                              visible only when `mode == "bse1"`.

            ivolx, ivoly, ivolz (int): Grid size parameters for the "Ivol" mode. These fields define the
                                       dimensions of the simulated volume and are visible only when
                                       `mode == "Ivol"`.

            ivolstepx, ivolstepy, ivolstepz (float): Step sizes for the "Ivol" mode. Defines the resolution
                                                     within the simulation volume.

            Various other parameters represent computational settings, such as:
              - num_el: Number of electrons.
              - platid, devid: IDs for the platform and device (e.g., OpenCL hardware).
              - globalworkgrpsz: Size of the global workgroup for parallel computations.
              - EkeV, Ehistmin, Ebinsize: Energy-related parameters for electron simulations.
              - depthmax, depthstep: Depth settings for the simulation.

            dataname, header, filename (str): Predefined paths and names for output data and configuration files.
            Notify (str): Toggle for notifications.

            no_quote_fields (tuple): Fields excluded from being quoted in the configuration file.

        Metadata:
            Metadata for certain fields (e.g., `mode`, `sig`, `sigstart`) includes information for controlling
            their visibility based on dependencies or user interface elements.
        """

        # Simulation mode with options and metadata for UI widgets
        mode: str = field(
            default="bse1",
            metadata={
                "widget": "combo",  # Specifies a combo box UI element
                "options": ["bse1", "full", "Ivol"],  # Available options for the simulation mode
                "visibility_controller": True,  # Indicates this field controls the visibility of others
            },
        )

        # Crystal name and grid size parameters
        xtalname: str = "GaN.xtal"  # Default crystal structure file name
        numsx: int = 501  # Number of x-direction grid points

        # Parameters specific to "full" mode
        sig: float = field(default=70.0, metadata={"visible_if": "full", "depends_on": "mode"})
        omega: float = field(default=0.0, metadata={"visible_if": "full", "depends_on": "mode"})

        # Parameters specific to "bse1" mode
        sigstart: float = field(default=0.0, metadata={"visible_if": "bse1", "depends_on": "mode"})
        sigend: float = field(default=30.0, metadata={"visible_if": "bse1", "depends_on": "mode"})
        sigstep: float = field(default=2.0, metadata={"visible_if": "bse1", "depends_on": "mode"})

        # Parameters specific to "Ivol" mode
        ivolx: int = field(default=1001, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivoly: int = field(default=1001, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivolz: int = field(default=101, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivolstepx: float = field(default=1.0, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivolstepy: float = field(default=1.0, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivolstepz: float = field(default=1.0, metadata={"visible_if": "Ivol", "depends_on": "mode"})

        # General simulation parameters
        num_el: int = 10  # Number of electrons
        platid: int = 1  # Platform ID (e.g., OpenCL platform)
        devid: int = 1  # Device ID (e.g., OpenCL device)
        globalworkgrpsz: int = 150  # Global workgroup size for parallel computations
        totnum_el: int = 200  # Total number of electrons
        multiplier: int = 1  # Multiplication factor for computations
        EkeV: float = 15.0  # Electron energy in keV
        Ehistmin: float = 14.0  # Minimum energy for histogram
        Ebinsize: float = 1.0  # Energy bin size
        depthmax: float = 100.0  # Maximum simulation depth
        depthstep: float = 1.0  # Depth step size

        # File paths and names
        dataname: str = field(default="EMFlow/temp/EMMCOpenCL/EMMCOpenCL.h5", init=False)  # Output data file path
        Notify: str = "Off"  # Notification toggle

        # Predefined header, filename, and fields excluded from quoting in the configuration file
        header: str = field(default="MCCLdata", init=False)
        filename: str = field(default="EMMCOpenCL.nml", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=tuple, init=False)

    # Instance of the nested `NML` dataclass, initialized by default
    nml: NML = field(default_factory=NML)
