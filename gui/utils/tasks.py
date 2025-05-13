from PyQt5.QtCore import QRunnable
from gui.forms.base.program_form import ProgramForm
from typing import List
from gui.utils.config_context import ConfigContext
import shutil

class SimulationTask(QRunnable):
    def __init__(self, program_forms: List[ProgramForm]):
        super().__init__()
        self.program_forms = program_forms

    def run(self):
        for program_form in self.program_forms:
            program_form: ProgramForm
            program_form.run_program()

        timestamped_folder = ConfigContext.get_timestamped_folder()
        temp_config_path = ConfigContext.get_data_path() / "EMFlow" / "temp"
        shutil.copytree(str(temp_config_path), str(timestamped_folder), dirs_exist_ok=True)

        print(f"[INFO] Output copied to {timestamped_folder}")

