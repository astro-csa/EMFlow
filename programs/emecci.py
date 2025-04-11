from base.emsoft_program import EMSoftProgram
from parameters.emecci import EMECCIParameters
from programs.emecp import EMECP

class EMECCI(EMSoftProgram):
    name = "EMECCI"
    config_class = EMECCIParameters

    def __init__(self, config: config_class):
        super().__init__(name=self.name, config=config)
        self.copy_input = EMECP