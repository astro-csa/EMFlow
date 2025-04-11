from base.emsoft_program import EMSoftProgram
from parameters.emmcopencl import EMMCOpenCLParameters

class EMMCOpenCL(EMSoftProgram):
    name = "EMMCOpenCL"
    config_class = EMMCOpenCLParameters

    def __init__(self, config: config_class):
        super().__init__(name=self.name, config=config)
        self.copy_input = False