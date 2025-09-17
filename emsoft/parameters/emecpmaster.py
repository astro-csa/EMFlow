from dataclasses import dataclass, field

from emsoft.common.emsoft_config import EMSoftConfig


@dataclass
class EMECPmasterParameters(EMSoftConfig):
    """
    Dataclass representing the configuration parameters for the `EMECPmaster` program.

    This class contains nested dataclasses (`BETHE` and `NML`) that store specific configurations for
    the program. Each nested dataclass defines structured parameters, default values, and additional
    metadata for file handling and UI integration.

    Attributes:
        - bethe (BETHE): Represents parameters related to the Bethe parameters for electron scattering.
        - nml (NML): Represents parameters for the `.nml` file configuration of the `EMECPmaster` program.
    """

    @dataclass
    class BETHE:
        """
        Nested dataclass for Bethe parameters related to electron scattering.

        Attributes:
            - c1, c2, c3 (float): Coefficients for Bethe parameters.
            - sgdbdiff (float): A parameter controlling scattering or database differences.
            - header (str): Predefined header for the configuration file, used when writing to `.nml`.
            - filename (str): Name of the Bethe parameters configuration file.
            - no_quote_fields (tuple): Fields excluded from being quoted in the output configuration file.
        """

        # Coefficients for Bethe parameters
        c1: float = 4.0  # Bethe coefficient 1
        c2: float = 8.0  # Bethe coefficient 2
        c3: float = 50.0  # Bethe coefficient 3

        # Database difference parameter
        sgdbdiff: float = 1.0  # Represents scattering database variation

        # Predefined header and file paths
        header: str = field(default="Bethelist", init=False)  # Header for the Bethe parameters section
        filename: str = field(default="BetheParameters.nml", init=False)  # Filename for the .nml file

        # Fields excluded from being quoted in the configuration file
        no_quote_fields: tuple[str, ...] = field(default_factory=tuple, init=False)

    @dataclass
    class NML:
        """
        Nested dataclass for `.nml` file parameters specific to the `EMECPmaster` program.

        Attributes:
            - npx (int): Number of points in the x-direction for simulations.
            - dmin (float): Minimum distance for computations.
            - copyfromenergyfile (str): File path for energy data to be copied into the current simulation.
            - energyfile (str): Predefined path for the program's output energy data.
            - combinesites (bool): Whether to combine computational sites.
            - Notify (str): Notification toggle for the program (e.g., "On" or "Off").
            - nthreads (int): Number of threads to use for the computation.
            - header (str): Predefined header for the `.nml` file section.
            - filename (str): Name of the `.nml` file.
            - no_quote_fields (tuple): Fields excluded from being quoted in the configuration file.
        """

        # Simulation parameters
        npx: int = 500  # Number of grid points in the x-direction
        dmin: float = 0.5  # Minimum distance for computations

        # Energy file handling
        copyfromenergyfile: str = "undefined"  # Path to the energy file for copying (if any)
        energyfile: str = field(default="EMFlow/temp/EMECPmaster/EMECPmaster.h5", init=False)  # Default path for the energy file output

        # Additional computation settings
        combinesites: bool = False  # Flag to enable or disable combining computational sites
        Notify: str = "Off"  # Notification toggle ("On" or "Off")
        nthreads: int = 12  # Number of threads for parallel computation

        # Predefined header and file metadata
        header: str = field(default="ECPmastervars", init=False)  # Header for the `.nml` configuration section
        filename: str = field(default="EMECPmaster.nml", init=False)  # Filename for the `.nml` file

        # Fields excluded from quoting in the configuration file
        no_quote_fields: tuple[str, ...] = field(default_factory=tuple, init=False)

    # Instances of the nested `BETHE` and `NML` dataclasses
    bethe: BETHE = field(default_factory=BETHE)  # Default instance of the Bethe configuration
    nml: NML = field(default_factory=NML)  # Default instance of the `.nml` configuration
