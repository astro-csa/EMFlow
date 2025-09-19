from __future__ import annotations

from typing import List

from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ui.forms.common.program_form import ProgramForm
from ui.utils.defaults_manager import load_defaults, save_defaults
from emsoft.common.emsoft_experiment import EMSoftExperiment


class DefaultValuesDialog(QDialog):
    """Dialog that renders a `ProgramForm` for each program in the given experiment."""

    def __init__(self, experiment: EMSoftExperiment, parent=None) -> None:
        super().__init__(parent)

        self._experiment = experiment
        self._program_forms: List[ProgramForm] = []
        self._experiment_name = experiment.name

        self.setWindowTitle(f"Modify Default Values - {experiment.name}")
        self.resize(900, 600)

        outer_layout = QVBoxLayout(self)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        outer_layout.addWidget(scroll)

        container = QWidget(scroll)
        scroll.setWidget(container)

        content_layout = QVBoxLayout(container)

        for step_name, program_class, config in experiment.steps:
            program_name = getattr(program_class, "name", step_name)
            persisted_config = load_defaults(
                self._experiment_name,
                program_name,
                type(config),
            )
            form = ProgramForm(
                type(config),
                program_class,
                # Capture the program name for this specific form instance
                on_generate=lambda f, n=program_name: self._apply_defaults(f, n),
                generate_label="Update Defaults",
            )
            if persisted_config is not None:
                form.load_config(persisted_config)
            group = QGroupBox(step_name, container)
            group_layout = QVBoxLayout(group)
            group_layout.addWidget(form)
            group.setLayout(group_layout)

            content_layout.addWidget(group)
            self._program_forms.append(form)

        content_layout.addStretch(1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        outer_layout.addWidget(buttons)

    @property
    def program_forms(self) -> List[ProgramForm]:
        """Expose the instantiated program forms for future use."""

        return self._program_forms

    def _apply_defaults(
        self,
        form: ProgramForm,
        program_name: str,
    ) -> None:
        config = form.get_config()
        path = save_defaults(self._experiment_name, program_name, config)
        print(f"[{program_name}] Saved default configuration to {path}")
