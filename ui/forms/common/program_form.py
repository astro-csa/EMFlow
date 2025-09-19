from __future__ import annotations

from collections.abc import Callable
from dataclasses import fields, is_dataclass
from typing import Optional

from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout, QWidget

from emsoft.common.emsoft_config import EMSoftConfig
from emsoft.common.emsoft_program import EMSoftProgram
from ui.forms.common.dataclass_form import DataclassForm
from ui.forms.programs.emecci_defect_form import DefectForm
from ui.forms.programs.emecci_foil_form import FoilForm


class ProgramForm(QWidget):
    """
    A GUI widget for configuring and executing an EMsoft program.

    The form dynamically reflects the structure of the program's configuration dataclass.
    Each nested dataclass becomes its own tab, while specialised sections such as FOIL or
    DEFECT rely on dedicated editor widgets. The generate button can be reused in different
    contexts by supplying a custom callback and label.

    Attributes:
        config_class: Dataclass describing the program configuration.
        program_class: Program type associated with the form.
        form_widgets (dict[str, QWidget]): Mapping of field names to their editor widgets.
        tabs (QTabWidget): Container holding the generated editors.
        generate_button (QPushButton): Trigger whose behaviour can be overridden via callback.
    """

    def __init__(
        self,
        config_class: type[EMSoftConfig],
        program_class: type[EMSoftProgram],
        on_generate: Optional[Callable[[ProgramForm], None]] = None,
        *,
        generate_label: str = "Generate Config",
    ) -> None:
        """Build a form for `program_class` using `config_class` metadata."""
        super().__init__()

        self.config_class = config_class
        self.program_class = program_class
        # Optional callback lets containers override the generate button behaviour
        self._on_generate = on_generate
        self.form_widgets: dict[str, QWidget] = {}

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        for field_ in fields(config_class):
            if not field_.init:
                continue

            field_name = field_.name
            field_type = field_.type

            if field_name.upper() == "FOIL":
                form = FoilForm()
                self.tabs.addTab(form, field_name.upper())

            elif field_name.upper() == "DEFECT":
                form = DefectForm()
                self.tabs.addTab(form, field_name.upper())

            elif is_dataclass(field_type):
                form = DataclassForm(field_type)
                self.form_widgets[field_name] = form
                self.tabs.addTab(form, field_name.upper())

        layout.addWidget(self.tabs)

        self.generate_button = QPushButton(generate_label)
        # Defer the clicked handling to a helper so we can branch on the callback
        self.generate_button.clicked.connect(self._handle_generate_clicked)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate_config(self) -> None:
        """Run the default config-generation workflow for the associated program."""
        try:
            config = self._get_config()
            program = self.program_class(config=config)
            program.generate_config()
        except Exception as exc:  # pragma: no cover - log surface for GUI users
            print(f"[ERROR] Failed to generate config: {exc}")

    def run_program(self) -> None:
        """Execute the program using the values captured by the form."""
        try:
            config = self._get_config()
            program = self.program_class(config=config)

            if program.update_input_name:
                program.copy_output_file(program.copy_output_from, program.name)
            elif program.copy_output_from:
                program.copy_output_file(program.copy_output_from)

            program.run()
        except Exception as exc:  # pragma: no cover - log surface for GUI users
            print(f"[ERROR] Error while running program: {exc}")

    def _get_config(self) -> EMSoftConfig:
        """Collect an updated configuration instance from the embedded widgets."""
        updated_config_data: dict[str, object] = {}

        for key, form in self.form_widgets.items():
            if isinstance(form, DataclassForm):
                updated_config_data[key] = form.get_instance()

        return self.config_class(**updated_config_data)

    def _handle_generate_clicked(self) -> None:
        """Dispatch the generate button click to a custom callback or the default logic."""
        if callable(self._on_generate):
            self._on_generate(self)
            return

        self.generate_config()

    def get_config(self) -> EMSoftConfig:
        """Expose the computed configuration so external callers can persist it."""

        return self._get_config()

    def load_config(self, config: EMSoftConfig) -> None:
        """Populate the form controls with values from an existing configuration."""

        for key, form in self.form_widgets.items():
            if not hasattr(config, key):
                continue

            value = getattr(config, key)
            if value is None:
                continue

            if isinstance(form, DataclassForm):
                form.set_instance(value)
