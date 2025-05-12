from PyQt5.QtCore import QRunnable
from gui.forms.base.program_form import ProgramForm
from typing import List

class SimulationTask(QRunnable):
    def __init__(self, program_forms: List[ProgramForm]):
        super().__init__()
        self.program_forms = program_forms

    def run(self):
        for program_form in self.program_forms:
            program_form: ProgramForm
            program_form.run_program()