from emsoft.common.emsoft_experiment import EMSoftExperiment
from emsoft.parameters.emecci import EMECCIParameters
from emsoft.parameters.emecp import EMECPParameters
from emsoft.parameters.emecpmaster import EMECPmasterParameters
from emsoft.parameters.emmcopencl import EMMCOpenCLParameters
from emsoft.programs.emecci import EMECCI
from emsoft.programs.emecp import EMECP
from emsoft.programs.emecpmaster import EMECPmaster
from emsoft.programs.emmcopencl import EMMCOpenCL

# Define the sequence of simulations to be performed
SIMULATIONS = {
    # First simulation type: "ECCI"
    "ECCI": EMSoftExperiment(
        name="ECCI",  # Name of the experiment
        steps=[
            # Step 1: EMMCOpenCL program with its parameters
            ("EMMCOpenCL", EMMCOpenCL, EMMCOpenCLParameters()),
            # Step 2: EMECPmaster program with its parameters
            ("EMECPmaster", EMECPmaster, EMECPmasterParameters()),
            # Step 3: EMECP program with its parameters
            ("EMECP", EMECP, EMECPParameters()),
            # Step 4: EMECCI program with its parameters
            ("EMECCI", EMECCI, EMECCIParameters()),
        ],
    ),
    # Second simulation type: "ECP"
    "ECP": EMSoftExperiment(
        name="ECP",  # Name of the experiment
        steps=[
            # Step 1: EMMCOpenCL program with its parameters
            ("EMMCOpenCL", EMMCOpenCL, EMMCOpenCLParameters()),
            # Step 2: EMECPmaster program with its parameters
            ("EMECPmaster", EMECPmaster, EMECPmasterParameters()),
            # Step 3: EMECP program with its parameters
            ("EMECP", EMECP, EMECPParameters()),
        ],
    ),
}
