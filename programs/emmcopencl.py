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

    nml: NML

class EMMCOpenCL(EMSoftProgram):
    def __init__(self, config: EMMCOpenCLParameters):
        super().__init__(
            name="EMMCOpenCL",
            config=config.nml,
            block_name="MCCLdata",
            output_file="EMMCOpenCL.nml"
        )



def main():
    params = EMMCOpenCLParameters(
        nml=EMMCOpenCLParameters.NML(
            mode = 'bse1',
            xtalname = 'GaN.xtal',
            numsx = 501,
            sig = 70.0,
            omega = 0.0,
            sigstart = 0.0,
            sigend = 30.0,
            sigstep = 2.0,
            ivolx = 1001,
            ivoly = 1001,
            ivolz = 101,
            ivolstepx = 1.0,
            ivolstepy = 1.0,
            ivolstepz = 1.0,
            num_el = 10,
            platid = 1,
            devid = 1,
            globalworkgrpsz = 150,
            totnum_el = 2000000000,
            multiplier = 1,
            EkeV = 15.0,
            Ehistmin = 14.0,
            Ebinsize = 1.0,
            depthmax = 100.0,
            depthstep = 1.0,
            dataname = 'GaN/EMMCOpenCL/_default/EMMCOpenCL.h5',
            Notify = 'Off'
        )
    )

if __name__ == "__main__":
    main()