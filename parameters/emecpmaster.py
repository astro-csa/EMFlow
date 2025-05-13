from dataclasses import dataclass, field

@dataclass
class EMECPmasterParameters:
    
    @dataclass
    class BETHE:
        c1: float = 4.0
        c2: float = 8.0
        c3: float = 50.0
        sgdbdiff: float = 1.0

        header: str = field(default="Bethelist", init=False)
        filename: str = field(default="BetheParameters.nml", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:[], init=False)

    @dataclass
    class NML:
        npx: int = 500
        dmin: float = 0.5
        copyfromenergyfile: str = "undefined"
        energyfile: str = field(default="EMFlow/temp/EMECPmaster/EMECPmaster.h5", init=False)
        combinesites: bool = False
        Notify: str = "Off"
        nthreads: int = 12

        header: str = field(default="ECPmastervars", init=False)
        filename: str = field(default="EMECPmaster.nml", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:[], init=False)
    
    bethe: BETHE = field(default_factory=BETHE)
    nml: NML = field(default_factory=NML)