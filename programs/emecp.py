from base.emsoft_program import EMSoftProgram
from parameters.emecp import EMECPParameters
from programs.emecpmaster import EMECPmaster

class EMECP(EMSoftProgram):
    name = "EMECP"
    config_class = EMECPParameters

    
    def __init__(self, config: config_class):
        super().__init__(name=self.name, config=config)
        self.copy_input = EMECPmaster

    