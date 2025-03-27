from base import EMSoftProgram
from dataclasses import dataclass

@dataclass
class EMECPParameters:

    @dataclass
    class EULER:
        type: str
        num: int
        angles: str

        filename: str = "euler.txt"
    
    @dataclass
    class NML:
        xtalname: str
        npix: int
        thetac: float
        maskpattern: str
        energyfile: str
        masterfile: str
        anglefile: str
        eulerconvention: str
        gammavalue: float
        outputformat: str
        datafile: str
        tiff_prefix: str
        nthreads: int
        sampletilt: float
        workingdistance: float
        Rin: float
        Rout: float
        fn_f: str
        fn_s: str
        xtalname2: str
        gF: str
        gS: str
        tF: str
        tS: str
        dmin: float
        filmthickness: float
        filmfile: str
        subsfile: str

        header: str = "ECPlist"
        filename: str = "EMECP.nml"
        no_quote_fields: list[str] = ["fn_f", "fn_s", "gF", "gS", "tF", "tS"]
    
    euler: EULER
    nml: NML

class EMECP(EMSoftProgram):
    def __init__(self, config: EMECPParameters):
        super().__init__(
            name="EMECP",
            config=config,
        )