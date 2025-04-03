from base.emsoft_program import EMSoftProgram
from parameters.emecpmaster import EMECPmasterParameters

class EMECPmaster(EMSoftProgram):
    name = "EMECPmaster"
    config_class = EMECPmasterParameters

    def __init__(self, config: config_class):
        super().__init__(name=self.name, config=config)