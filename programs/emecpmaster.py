from base.emsoft_program import EMSoftProgram
from parameters.emecpmaster import EMECPmasterParameters
from programs.emmcopencl import EMMCOpenCL

class EMECPmaster(EMSoftProgram):
    name = "EMECPmaster"
    config_class = EMECPmasterParameters
    
    def __init__(self, config: config_class):
        super().__init__(name=self.name, config=config)
        self.copy_input = EMMCOpenCL
        self.update_input_name = True