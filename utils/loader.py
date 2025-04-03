import sys
import importlib
import inspect
from pathlib import Path
from typing import List, Tuple, Type
from base.emsoft_program import EMSoftProgram

# Add project root to sys.path
root = Path(__file__).resolve().parent.parent
sys.path.append(str(root))

def get_programs() -> List[Tuple[Type, str]]:
    program_dir = root / "programs"
    programs = []

    for file in program_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue

        module_name = file.stem

        try:
            module = importlib.import_module(f"programs.{module_name}")
        except Exception as e:
            print(f"[ERROR] Could not import module '{module_name}': {e}")
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, EMSoftProgram) and obj is not EMSoftProgram:
                try:
                    config_class = getattr(obj, "config_class", None)
                    if config_class is None:
                        print(f"[WARNING] No 'config' type hint found in class '{obj.__name__}'")
                        continue
                    
                    name = getattr(obj, "name", obj.__name__)
                    programs.append((config_class, obj, name))
                except Exception as e:
                    print(f"[ERROR] Problem extracting config class from '{obj.__name__}': {e}")
                break

    return programs
