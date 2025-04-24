from dataclasses import dataclass, field

@dataclass
class EMECCIParameters:
    
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
        nthreads: int = 12
        voltage: float = 15.0
        xtalname: str = "GaN.xtal"
        progmode: str = "array"
        summode: str = "diag"
        k: str = "0,0,1"
        dkt: float = 1.5
        ktmax: float = 3.0
        lauec: str = "0.0, 0.0"
        lauec2: str = "0.0, 0.0"
        nktstep: int = 20
        dmin: float = 0.5
        defectfilename: str = "EMECCI/EMdefect.json"
        dataname: str = "EMECCI/EMECCI.h5"
        ECPname: str = "EMECCI/EMECP.h5"
        montagename: str = "EMECCI/EMECCI.tiff"
        DF_L: float = 1.0
        DF_npix: int = 256
        DF_npiy: int = 256
        DF_slice: float = 1.0

        header: str = field(default="ECCIlist", init=False)
        filename: str = field(default="EMECCI.nml", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:["k", "lauec", "lauec2"], init=False)
    
    @dataclass
    class FOIL:
        foil_path: str = "EMECCI/EMfoil.json"

        #filename: str = field(default="EMfoil.json", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:[], init=False)

    @dataclass
    class DEFECT:
        defect_path: str = "EMECCI/EMdefect.json"

        #filename: str = field(default="EMdefect.json", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:[], init=False)

    bethe: BETHE = field(default_factory=BETHE)
    nml: NML = field(default_factory=NML)
    foil: FOIL = field(default_factory=FOIL)
    defect: DEFECT = field(default_factory=DEFECT)