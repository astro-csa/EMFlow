from dataclasses import dataclass, field

from emsoft.common.emsoft_config import EMSoftConfig


@dataclass
class EMECCIParameters(EMSoftConfig):
    """
    Dataclass representing the configuration parameters for the `EMECCI` program.

    This class contains multiple nested dataclasses (`BETHE`, `NML`, `FOIL`, `DEFECT`) to logically
    group related parameters for the program. Each section handles specific configurations, such as
    Bethe scattering parameters, `.nml` configuration, foil settings, and defect settings.

    Attributes:
        - bethe (BETHE): Bethe parameters for electron scattering.
        - nml (NML): Parameters for the `.nml` configuration file.
        - foil (FOIL): Parameters related to the foil configuration.
        - defect (DEFECT): Parameters related to defect configuration.
    """

    @dataclass
    class BETHE:
        """
        Nested dataclass for Bethe scattering parameters.

        Attributes:
            - c1, c2, c3 (float): Coefficients for the Bethe scattering calculations.
            - sgdbdiff (float): A parameter controlling database differences for scattering.
            - header (str): Header for the Bethe parameters section in the `.nml` file.
            - filename (str): File name for saving the Bethe parameters.
            - no_quote_fields (tuple): Fields excluded from being quoted in the configuration file.
        """

        c1: float = 4.0  # Bethe coefficient 1
        c2: float = 8.0  # Bethe coefficient 2
        c3: float = 50.0  # Bethe coefficient 3
        sgdbdiff: float = 1.0  # Scattering database difference parameter

        # Metadata for output configuration
        header: str = field(default="Bethelist", init=False)  # Section header in the `.nml` file
        filename: str = field(default="BetheParameters.nml", init=False)  # Name of the Bethe parameters file
        no_quote_fields: tuple[str, ...] = field(default_factory=tuple, init=False)  # No quoted fields

    @dataclass
    class NML:
        """
        Nested dataclass for `.nml` configuration parameters.

        Attributes:
            - nthreads (int): Number of threads for parallel computation.
            - voltage (float): Operating voltage in kilovolts (kV).
            - xtalname (str): Name of the crystal structure file.
            - progmode, summode (str): Program and summation modes.
            - k (str): Vector representing the beam direction.
            - dkt, ktmax (float): Parameters controlling the k-space grid.
            - lauec, lauec2 (str): Laue circle parameters as vectors.
            - nktstep (int): Number of steps in the k-space grid.
            - File paths for defect, data, ECP, and montage output files.
            - Additional parameters for dark field (DF) simulation.
            - Metadata for `.nml` file generation (e.g., `header`, `filename`).

        Metadata:
            Metadata is added for certain fields to facilitate GUI rendering, such as defining vector inputs.
        """

        nthreads: int = 12  # Number of threads for parallel computation
        voltage: float = 15.0  # Operating voltage in kilovolts (kV)
        xtalname: str = "GaN.xtal"  # Name of the crystal structure file
        progmode: str = "array"  # Program mode (e.g., "array" mode)
        summode: str = "diag"  # Summation mode (e.g., "diag" mode)

        # Vector fields with metadata for GUI rendering
        k: str = field(default="", metadata={"widget": "vector", "size": 3, "default_value": "0, 0, 1"})  # Beam direction vector

        # Parameters for k-space grid
        dkt: float = 1.5  # Increment in k-space
        ktmax: float = 3.0  # Maximum k-space value
        lauec: str = field(default="", metadata={"widget": "vector", "size": 2, "default_value": "0.0, 0.0"})  # Laue circle center
        lauec2: str = field(default="", metadata={"widget": "vector", "size": 2, "default_value": "0.0, 0.0"})  # Second Laue circle center
        nktstep: int = 20  # Number of steps in k-space

        # Simulation parameters
        dmin: float = 0.5  # Minimum distance for computations
        defectfilename: str = field(default="EMFlow/temp/EMECCI/EMdefect.json", init=False)  # Defect file path
        dataname: str = field(default="EMFlow/temp/EMECCI/EMECCI.h5", init=False)  # Data output file path
        ECPname: str = field(default="EMFlow/temp/EMECCI/EMECP.h5", init=False)  # ECP file path
        montagename: str = field(default="EMFlow/temp/EMECCI/EMECCI.tiff", init=False)  # TIFF file output path

        # Parameters for dark field (DF) simulation
        DF_L: float = 1.0  # Length scale for dark field simulation
        DF_npix: int = 256  # Number of pixels in x-direction for DF computation
        DF_npiy: int = 256  # Number of pixels in y-direction for DF computation
        DF_slice: float = 1.0  # Slice thickness for DF computation

        # Metadata for `.nml` configuration
        header: str = field(default="ECCIlist", init=False)  # Header for the `.nml` file
        filename: str = field(default="EMECCI.nml", init=False)  # Name of the `.nml` configuration file
        no_quote_fields: tuple[str, ...] = field(
            default_factory=lambda: ("k", "lauec", "lauec2"), init=False
        )  # Fields excluded from quoting in the output file

    @dataclass
    class FOIL:
        """
        Nested dataclass for foil configuration parameters.

        Attributes:
            - foil_path (str): Path to the foil configuration file.
            - no_quote_fields (tuple): Fields excluded from being quoted.
        """

        foil_path: str = "EMFlow/temp/EMECCI/EMfoil.json"  # Foil configuration file path
        no_quote_fields: tuple[str, ...] = field(default_factory=tuple, init=False)  # No quoted fields

    @dataclass
    class DEFECT:
        """
        Nested dataclass for defect configuration parameters.

        Attributes:
            - defect_path (str): Path to the defect configuration file.
            - no_quote_fields (tuple): Fields excluded from being quoted.
        """

        defect_path: str = "EMFlow/temp/EMECCI/EMdefect.json"  # Defect configuration file path
        no_quote_fields: tuple[str, ...] = field(default_factory=tuple, init=False)  # No quoted fields

    # Instances of the nested dataclasses
    bethe: BETHE = field(default_factory=BETHE)  # Default instance of Bethe parameters
    nml: NML = field(default_factory=NML)  # Default instance of `.nml` parameters
    foil: FOIL = field(default_factory=FOIL)  # Default instance of foil parameters
    defect: DEFECT = field(default_factory=DEFECT)  # Default instance of defect parameters
