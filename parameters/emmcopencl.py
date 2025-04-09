from dataclasses import dataclass, field

@dataclass
class EMMCOpenCLParameters:

    @dataclass
    class NML:
        mode: str = field(default="bse1", metadata={"widget": "combo", "options": ["bse1", "full", "Ivol"], "visibility_controller": True})
        
        xtalname: str = "GaN.xtal"
        numsx: int = 501
        
        sig: float = field(default=70.0, metadata={"visible_if": "full", "depends_on": "mode"})
        omega: float = field(default=0.0, metadata={"visible_if": "full", "depends_on": "mode"})
        
        sigstart: float = field(default=0.0, metadata={"visible_if": "bse1", "depends_on": "mode"})
        sigend: float = field(default=30.0, metadata={"visible_if": "bse1", "depends_on": "mode"})
        sigstep: float = field(default=2.0, metadata={"visible_if": "bse1", "depends_on": "mode"})
        
        ivolx: int = field(default=1001, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivoly: int = field(default=1001, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivolz: int = field(default=101, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivolstepx: float = field(default=1.0, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivolstepy: float = field(default=1.0, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        ivolstepz: float = field(default=1.0, metadata={"visible_if": "Ivol", "depends_on": "mode"})
        
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
