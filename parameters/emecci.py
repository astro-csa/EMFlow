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
        k: str = field(default="", metadata={"widget": "vector", "size": 3, "default_value": "0, 0, 1"})
        dkt: float = 1.5
        ktmax: float = 3.0
        lauec: str = field(default="", metadata={"widget": "vector", "size": 2, "default_value": "0.0, 0.0"})
        lauec2: str = field(default="", metadata={"widget": "vector", "size": 2, "default_value": "0.0, 0.0"})
        nktstep: int = 20
        dmin: float = 0.5
        defectfilename: str = field(default="EMFlow/temp/EMECCI/EMdefect.json", init=False)
        dataname: str = field(default="EMFlow/temp/EMECCI/EMECCI.h5", init=False)
        ECPname: str = field(default="EMFlow/temp/EMECCI/EMECP.h5", init=False)
        montagename: str = field(default="EMFlow/temp/EMECCI/EMECCI.tiff", init=False)
        DF_L: float = 1.0
        DF_npix: int = 256
        DF_npiy: int = 256
        DF_slice: float = 1.0

        header: str = field(default="ECCIlist", init=False)
        filename: str = field(default="EMECCI.nml", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:["k", "lauec", "lauec2"], init=False)
    
    @dataclass
    class FOIL:
        foil_path: str = "EMFlow/temp/EMECCI/EMfoil.json"

        #filename: str = field(default="EMfoil.json", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:[], init=False)

    @dataclass
    class DEFECT:
        defect_path: str = "EMFlow/temp/EMECCI/EMdefect.json"

        #filename: str = field(default="EMdefect.json", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:[], init=False)

    bethe: BETHE = field(default_factory=BETHE)
    nml: NML = field(default_factory=NML)
    foil: FOIL = field(default_factory=FOIL)
    defect: DEFECT = field(default_factory=DEFECT)