from base import EMSoftProgram
from dataclasses import dataclass

@dataclass
class EMECPmasterParameters:
    
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
        npx: int
        dmin: float
        copyfromenergyfile: str
        energyfile: str
        combinesites: bool
        Notify: str
        nthreads: int

        header: str = "ECPmastervars"
        filename: str = "EMECPmaster.nml"
    
    bethe: BETHE
    nml: NML

class EMECPmaster(EMSoftProgram):
    def __init__(self, config: EMECPmasterParameters):
        super().__init__(
            name="EMECPmaster",
            config=config,
        )