from dataclasses import dataclass, field

@dataclass
class EMECPParameters:

    @dataclass
    class EULER:
        type: str = "eu"
        num: int = 1
        angles: str = "0,0,0"

        filename: str = field(default="euler.txt", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:["angles"], init=False)
    
    @dataclass
    class NML:
        xtalname: str = "GaN.xtal"
        npix: int = 256
        thetac: float = 5.0
        maskpattern: str = "n"
        energyfile: str = "EMECP/EMECPmaster.h5"
        masterfile: str = "EMECP/EMECPmaster.h5"
        anglefile: str = "EMECP/euler.txt"
        eulerconvention: str = "hkl"
        gammavalue: float = 1.0
        outputformat: str = "bin"
        datafile: str = "EMECP/EMECP.h5"
        tiff_prefix: str = "undefined"
        nthreads: int = 12
        sampletilt: float = 0.0
        workingdistance: float = 13.0
        Rin: float = 2.0
        Rout: float = 6.0
        fn_f: str = "0,0,1"
        fn_s: str = "0,0,1"
        xtalname2: str = "undefined"
        gF: str = "0,0,0"
        gS: str = "0,0,0"
        tF: str = "0,0,0"
        tS: str = "0,0,0"
        dmin: float = 0.025
        filmthickness: float = 0.0
        filmfile: str = "undefined"
        subsfile: str = "undefined"

        header: str = field(default="ECPlist", init=False)
        filename: str = field(default="EMECP.nml", init=False)
        no_quote_fields: tuple[str, ...] = field(default_factory=lambda:["fn_f", "fn_s", "gF", "gS", "tF", "tS"], init=False)
    
    euler: EULER = field(default_factory=EULER)
    nml: NML = field(default_factory=NML)