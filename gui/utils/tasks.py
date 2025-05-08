from PyQt5.QtCore import QRunnable, pyqtSlot
from base.experiment import Experiment

class SimulationTask(QRunnable):
    def __init__(self, experiment: Experiment):
        super().__init__()
        self.experiment = experiment

    @pyqtSlot()
    def run(self):
        print(f"[INFO] Executing {self.experiment.name}")
        for step_name, program_class, config in self.experiment.steps:
            program = program_class(config)
            print(f"[RUNNING] {step_name}")
            #program.generate_config()
            program.run()
            print(f"[DONE] {step_name}")
        print(f"[COMPLETE] Simulation {self.experiment.name} complete.")