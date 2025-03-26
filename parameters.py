from dataclasses import dataclass

@dataclass
class EMMCOpenCLParameters:
    #EMMCOpenCL.nml
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

@dataclass
class EMECPmasterParameters:
    #BetheParameters.nml
    c1: float
    c2: float
    c3: float
    sgdbdiff: float
    #EMECPmaster.nml
    npx: int
    dmin: float
    copyfromenergyfile: str
    energyfile: str
    combinesites: bool
    Notify: str
    nthreads: int

@dataclass
class EMECPParameters:
    #Euler.txt
    type: str
    num: int
    anglex: float
    angley: float
    anglez: float
    #EMECP.nml
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

@dataclass
class EMECCIParameters:
    #EMdefect.json
    EMdefectPath: str
    #EMfoil.json
    EMfoilPath: str
    #BetheParameters.nml
    c1: float
    c2: float
    c3: float
    sgdbdiff: float
    #EMECCI.nml
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