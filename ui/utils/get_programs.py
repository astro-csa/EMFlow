import inspect
import sys
from pathlib import Path

# Import the EMSoftProgram base class to identify program classes
from emsoft.common.emsoft_program import EMSoftProgram

# Set up the root directory path relative to the current file
root = Path(__file__).resolve().parent.parent
program_dir = root / "programs"  # Directory containing program modules


def get_programs():
    """
    Scans the 'programs' directory for Python files and extracts all classes that inherit
    from the `EMSoftProgram` base class. This function dynamically identifies all available
    simulation programs and their associated configuration classes.

    Returns:
        list[tuple]: A list of tuples, where each tuple contains:
            - config_class: The configuration dataclass for the program.
            - program_class: The class representing the program (subclass of `EMSoftProgram`).
            - program_name: The name of the program (stored in the `name` attribute of the class).

    Notes:
        - Assumes all relevant modules in the `programs` directory are already imported.
        - This design enables dynamic discovery of programs without hardcoding their definitions.
    """
    available = []  # List to store discovered programs

    # Iterate through all Python files in the 'programs' directory
    for file in program_dir.glob("*.py"):
        if file.name == "__init__.py":  # Skip the __init__.py file
            continue

        module_name = file.stem  # Get the module name (filename without extension)

        # Retrieve the module from the `sys.modules` dictionary (already imported)
        full_module_name = f"programs.{module_name}"
        module = sys.modules.get(full_module_name)
        if not module:
            # Log a warning if the module was not imported
            print(f"[SKIPPED] Module {full_module_name} not loaded — expected to be imported by simulation_registry.")
            continue

        # Inspect the module for classes that inherit from EMSoftProgram
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, EMSoftProgram) and obj is not EMSoftProgram:
                # The class `obj` is a subclass of EMSoftProgram
                try:
                    # Extract the configuration class from the type hints of the class's `__init__` method
                    config = obj.__init__.__annotations__.get("config")  # Extract the "config" type hint
                    # Append the configuration class, program class, and program name to the list
                    available.append((config, obj, obj.name))
                except Exception as e:
                    # Log a warning if the configuration class cannot be extracted
                    print(f"[WARNING] Failed to extract config for {obj}: {e}")
                break  # Only process the first subclass found in the module

    # Return the list of discovered programs
    return available
