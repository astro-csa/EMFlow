import programs.emecci
import programs.emecp
import programs.emecpmaster
import programs.emmcopencl

from base.experiment import Experiment

from programs.emmcopencl import EMMCOpenCL
from parameters.emmcopencl import EMMCOpenCLParameters

from programs.emecpmaster import EMECPmaster
from parameters.emecpmaster import EMECPmasterParameters

from programs.emecp import EMECP
from parameters.emecp import EMECPParameters

from programs.emecci import EMECCI
from parameters.emecci import EMECCIParameters

SIMULATIONS = {
    "ECCI": Experiment(
        name="ECCI",
        steps=[
            ("EMMCOpenCL", EMMCOpenCL, EMMCOpenCLParameters()),
            ("EMECPmaster", EMECPmaster, EMECPmasterParameters()),
            ("EMECP", EMECP, EMECPParameters()),
            ("EMECCI", EMECCI, EMECCIParameters()),
        ]
    ),
    "ECP": Experiment(
        name="ECP",
        steps=[
            ("EMMCOpenCL", EMMCOpenCL, EMMCOpenCLParameters()),
            ("EMECPmaster", EMECPmaster, EMECPmasterParameters()),
            ("EMECP", EMECP, EMECPParameters()),
        ]
    )
}
