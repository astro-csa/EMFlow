from base import EMSoftProgram
from dataclasses import dataclass

@dataclass
class EMMCOpenCLParameters:

    @dataclass
    class NML:
        mode: str
        xtalname: str
        numsx: int
        sig: float
        omega: float
        sigstart: float
        sigend: float
        sigstep: float
        ivolx: int
        ivoly: int
        ivolz: int
        ivolstepx: float
        ivolstepy: float
        ivolstepz: float
        num_el: int
        platid: int
        devid: int
        globalworkgrpsz: int
        totnum_el: int
        multiplier: int
        EkeV: float
        Ehistmin: float
        Ebinsize: float
        depthmax: float
        depthstep: float
        dataname: str
        Notify: str

        header: str = "MCCLdata"
        filename: str = "EMMCOpenCL.nml"

    nml: NML

class EMMCOpenCL(EMSoftProgram):
    def __init__(self, config: EMMCOpenCLParameters):
        super().__init__(
            name="EMMCOpenCL",
            config=config,
        )