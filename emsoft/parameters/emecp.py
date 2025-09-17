from dataclasses import dataclass, field

from emsoft.common.emsoft_config import EMSoftConfig


@dataclass
class EMECPParameters(EMSoftConfig):
    """
    Dataclass representing the configuration parameters for the `EMECP` program.

    This class contains nested dataclasses (`EULER` and `NML`), which group specific configurations
    for the program. The `EULER` class stores parameters for Euler angles, while the `NML` class
    contains parameters for the `.nml` configuration file.

    Attributes:
        - euler (EULER): Nested dataclass for Euler angle parameters.
        - nml (NML): Nested dataclass for `.nml` configuration parameters.
    """

    @dataclass
    class EULER:
        """
        Nested dataclass for Euler angle configurations.

        Attributes:
            - type (str): The type of Euler angle representation (default is `"eu"`).
            - num (int): The number of Euler angles (default is `1`).
            - angles (str): A vector of Euler angles, represented as a string. Metadata is added
                            for GUI rendering as a "vector" widget with three components.
            - filename (str): The name of the file where Euler angles will be saved.
            - no_quote_fields (tuple): Specifies fields excluded from quoting in the configuration file.
        """

        # Euler angle configuration fields
        type: str = "eu"  # Euler angle type (e.g., "eu" for Euler angles)
        num: int = 1  # Number of defined Euler angles
        angles: str = field(
            default="",
            metadata={
                "widget": "vector",  # Indicates this field is a vector in GUI
                "size": 3,  # Specifies the number of components (x, y, z)
                "default_value": "0.0, 0.0, 0.0",  # Default vector value
            },
        )

        # Metadata for output configuration
        filename: str = field(default="euler.txt", init=False)  # Output file for Euler angles
        no_quote_fields: tuple[str, ...] = field(
            default_factory=lambda: ("angles",), init=False
        )  # Prevent quoting for the "angles" field in the output file

    @dataclass
    class NML:
        """
        Nested dataclass for `.nml` configuration parameters.

        Attributes:
            - xtalname (str): Name of the crystal structure file.
            - npix (int): Number of pixels for data simulation.
            - thetac (float): The tilt angle for the simulation in degrees.
            - maskpattern (str): Mask pattern for computations (e.g., "n" for no mask).
            - energyfile and masterfile (str): Paths to the energy file and master file, respectively.
            - anglefile (str): Path to the Euler angle data file.
            - eulerconvention (str): The convention used for Euler angles (e.g., `"hkl"`).
            - Various fields (e.g., `fn_f`, `fn_s`, `gF`, `gS`, `tF`, `tS`) represent vectors used in
              data processing and are defined with metadata for GUI rendering.
            - dmin (float): Minimum distance for computations.
            - filmthickness (float): Thickness of the film in the simulation.
            - filmfile/subsfile (str): Filenames for film and substrate files.
            - Metadata fields for `.nml` configuration (e.g., `filename`, `header`) are predefined.

        Metadata:
            Metadata such as `widget` and `default_value` is added for specific fields to support
            GUI rendering and input handling.
        """

        # Basic simulation parameters
        xtalname: str = "GaN.xtal"  # Crystal structure file
        npix: int = 256  # Number of pixels in the simulation
        thetac: float = 5.0  # Tilt angle for the simulation in degrees
        maskpattern: str = "n"  # Mask pattern (e.g., "n" for no mask)

        # File paths for energy, master, and Euler files
        energyfile: str = field(default="EMFlow/temp/EMECP/EMECPmaster.h5", init=False)  # Energy file path
        masterfile: str = field(default="EMFlow/temp/EMECP/EMECPmaster.h5", init=False)  # Master file path
        anglefile: str = field(default="EMFlow/temp/EMECP/euler.txt", init=False)  # Euler angles file path

        # Additional simulation parameters
        eulerconvention: str = "hkl"  # Euler angle convention
        gammavalue: float = 1.0  # Gamma value for computations
        outputformat: str = "bin"  # Output data format
        datafile: str = field(default="EMFlow/temp/EMECP/EMECP.h5", init=False)  # Output data file path
        # tiff_prefix: str = "undefined"  # Prefix for output TIFF files (only in Linux)
        nthreads: int = 12  # Number of threads for computation
        sampletilt: float = 0.0  # Tilt of the sample in the simulation
        workingdistance: float = 13.0  # Working distance in mm
        Rin: float = 2.0  # Inner radius for computations
        Rout: float = 6.0  # Outer radius for computations

        # Vector fields with metadata for GUI rendering
        fn_f: str = field(default="", metadata={"widget": "vector", "size": 3, "default_value": "0, 0, 1"})  # Vector field for fn_f
        fn_s: str = field(default="", metadata={"widget": "vector", "size": 3, "default_value": "0, 0, 1"})  # Vector field for fn_s
        xtalname2: str = "undefined"  # Secondary crystal name
        gF: str = field(default="", metadata={"widget": "vector", "size": 3, "default_value": "0, 0, 0"})  # Vector field for gF
        gS: str = field(default="", metadata={"widget": "vector", "size": 3, "default_value": "0, 0, 0"})  # Vector field for gS
        tF: str = field(default="", metadata={"widget": "vector", "size": 3, "default_value": "0, 0, 0"})  # Vector field for tF
        tS: str = field(default="", metadata={"widget": "vector", "size": 3, "default_value": "0, 0, 0"})  # Vector field for tS

        # Film and substrate parameters
        dmin: float = 0.025  # Minimum distance for surface features
        filmthickness: float = 0.0  # Thickness of the film
        filmfile: str = "undefined"  # Path to the film file
        subsfile: str = "undefined"  # Path to the substrate file

        # Metadata for `.nml` configuration
        header: str = field(default="ECPlist", init=False)  # Header for `.nml` sections
        filename: str = field(default="EMECP.nml", init=False)  # Name of the `.nml` configuration file
        no_quote_fields: tuple[str, ...] = field(
            default_factory=lambda: ("fn_f", "fn_s", "gF", "gS", "tF", "tS"), init=False
        )  # Fields excluded from quoting in the output file

    # Instances of the nested dataclasses
    euler: EULER = field(default_factory=EULER)  # Default instance of Euler configuration
    nml: NML = field(default_factory=NML)  # Default instance of `.nml` configuration
