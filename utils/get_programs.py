import sys
import inspect
from pathlib import Path
from typing import List, Tuple, Type

from base.emsoft_program import EMSoftProgram

# This import is only to ensure that all programs and parameters are imported
# so PyInstaller can bundle them properly
import simulations.simulation_registry

# Set up the root path
root = Path(__file__).resolve().parent.parent
program_dir = root / "programs"

def get_programs() -> List[Tuple[Type, Type[EMSoftProgram], str]]:
    """
    Returns a list of (config_class, program_class, program_name) tuples
    by scanning the 'programs' directory and extracting all classes that
    inherit from EMSoftProgram. Assumes all relevant modules were already imported.
    """
    available = []

    for file in program_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue

        module_name = file.stem

        # Get the module from sys.modules (already imported)
        full_module_name = f"programs.{module_name}"
        module = sys.modules.get(full_module_name)
        if not module:
            print(f"[SKIPPED] Module {full_module_name} not loaded — expected to be imported by simulation_registry.")
            continue

        # Look for a subclass of EMSoftProgram
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, EMSoftProgram) and obj is not EMSoftProgram:
                try:
                    config = obj.__init__.__annotations__.get("config")  # type hint
                    available.append((config, obj, obj.name))
                except Exception as e:
                    print(f"[WARNING] Failed to extract config for {obj}: {e}")
                break

    return available