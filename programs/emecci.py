from base import EMSoftProgram
from dataclasses import dataclass

@dataclass
class EMECCIParameters:
    
    @dataclass
    class BETHE:
        c1: float
        c2: float
        c3: float
        sgdbdiff: float

        header: str = "Bethelist"
        filename: str = "BetheParameters.nml"

    @dataclass
    class NML:
        nthreads: int
        voltage: float
        xtalname: str
        progmode: str
        summode: str
        k: str
        dkt: float
        ktmax: float
        lauec: str
        lauec2: str
        nktstep: int
        dmin: float
        defectfilename: str
        dataname: str
        ECPname: str
        montagename: str
        DF_L: float
        DF_npix: int
        DF_npiy: int
        DF_slice: float

        header: str = "ECCIlist"
        filename: str = "EMECCI.nml"

    #defect_path: str
    #foil_path: str
    bethe: BETHE
    nml: NML

class EMECCI(EMSoftProgram):
    def __init__(self, config: EMECCIParameters):
        super().__init__(
            name="EMECCI",
            config=config,
        )