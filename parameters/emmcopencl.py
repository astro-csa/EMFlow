from dataclasses import dataclass, field

@dataclass
class EMMCOpenCLParameters:

    @dataclass
    class NML:
        mode: str = "bse1"
        xtalname: str = "GaN.xtal"
        numsx: int = 501
        sig: float = 70.0
        omega: float = 0.0
        sigstart: float = 0.0
        sigend: float = 30.0
        sigstep: float = 2.0
        ivolx: int = 1001
        ivoly: int = 1001
        ivolz: int = 101
        ivolstepx: float = 1.0
        ivolstepy: float = 1.0
        ivolstepz: float = 1.0
        num_el: int = 10
        platid: int = 1
        devid: int = 1
        globalworkgrpsz: int = 150
        totnum_el: int = 200
        multiplier: int = 1
        EkeV: float = 15.0
        Ehistmin: float = 14.0
        Ebinsize: float = 1.0
        depthmax: float = 100.0
        depthstep: float = 1.0
        dataname: str = "EMMCOpenCL/EMMCOpenCL.h5"
        Notify: str = "Off"

        header: str = field(default="MCCLdata", init=False)
        filename: str = field(default="EMMCOpenCL.nml", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:[], init=False)

    nml: NML = field(default_factory=NML)
