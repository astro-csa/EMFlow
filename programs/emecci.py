from base import EMSoftProgram
from dataclasses import dataclass, field

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
        no_quote_fields: list[str] = field(default_factory=lambda:[])

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
        no_quote_fields: list[str] = field(default_factory=lambda:["k", "lauec", "lauec2"])

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