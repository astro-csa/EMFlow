import subprocess
import shutil
from dataclasses import asdict, is_dataclass
from pathlib import Path

class EMSoftProgram:
    """
    Abstract base class for all EMSoft program wrappers.

    Subclasses should implement or inherit the following methods:
    - generate_config(): Generate all necessary .nml/.json files for the program.
    - run(): Optionally execute the program with the generated configuration.

    This class provides shared logic for all EMFlow program wrappers.
    """
    def __init__(self, name: str, config: object):
        self.name = name
        self.config = config
        self.copy_output_from = None
        self.update_input_name = False

    def generate_config(self):
        """
        Generate the configuration files needed to run the EMSoft program.
        This method should be called after setting all required parameters.
        """
        for attr_name in self.config.__dataclass_fields__:
            attr = getattr(self.config, attr_name)
            if is_dataclass(attr):
                self._generate_config_file(attr)
    
    def copy_output_file(self, source_program: "EMSoftProgram", new_name: str = None) -> None:
        original_name = f"{source_program.name}.h5"
        source_path = Path(source_program.name) / original_name

        target_dir = Path(self.name)
        target_dir.mkdir(parents=True, exist_ok=True)

        target_filename = f"{new_name}.h5" if new_name else original_name
        target_path =target_dir / target_filename

        shutil.copy2(source_path, target_path)
        print(f"[{self.name}] Copied {original_name} from {source_program.name}/ as {target_filename}")
        

    def run(self):
        executable = self.name
        main_config_path = self._get_main_config_file()

        if not main_config_path.exists():
            print(f"[{self.name}] ❌ Config file not found: {main_config_path}")
            return

        print(f"[{self.name}] ▶️ Running: {executable} {main_config_path.name}")

        # Use subprocess.Popen with unbuffered output
        process = subprocess.Popen(
            [executable, main_config_path.name],
            cwd=main_config_path.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,        # Decode bytes to strings
            bufsize=1         # Enable line-buffered output
        )

        # Read stdout and stderr line by line
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(f"[{self.name}] [STDOUT]: {output.strip()}")

        # Handle any remaining stderr
        error_output = process.stderr.read()
        if error_output:
            print(f"[{self.name}] [STDERR]: {error_output.strip()}")

        # Check return code
        if process.returncode == 0:
            print(f"[{self.name}] ✅ Execution completed.")
        else:
            print(f"[{self.name}] ❌ Execution failed with code {process.returncode}")

    def _generate_config_file(self, section: object) -> str:
        header = getattr(section, "header", None)
        filename = getattr(section, "filename", None)
        no_quote_fields = getattr(section, "no_quote_fields", [])

        if not filename:
            return
        
        data = asdict(section)

        if header:
            lines = [f"&{header}"]
        else:
            lines = []

        if filename.lower() == "euler.txt":
            for key, value in data.items():
                if key in ["header", "filename", "no_quote_fields"]:
                    continue
                lines.append(f"{value}")

        else:
            for key, value in data.items():
                if key in ["header", "filename", "no_quote_fields"]:
                    continue
                formatted = self._format_value(key, value, no_quote_fields)
                lines.append(f" {key} = {formatted},")
            lines.append("/")
        
        output_dir = Path(self.name)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        output_path.write_text("\n".join(lines) + "\n")
        print(f"[{self.name}] {output_path} generated.")

    def _get_main_config_file(self) -> Path:
        """Busca el archivo .nml que tiene el mismo nombre que el programa."""
        for attr_name in self.config.__dataclass_fields__:
            section = getattr(self.config, attr_name)
            if is_dataclass(section):
                filename = getattr(section, "filename", None)
                if filename and filename.startswith(self.name):
                    return Path(self.name) / filename
        # Fallback: simplemente asume nombre estándar
        return Path(self.name) / f"{self.name}.nml"

    def _format_value(self, key, value, no_quote_fields):
        if isinstance(value, str):
            if key in no_quote_fields:
                return value
            else:
                return f"'{value}'"
        elif isinstance(value, bool):
            return ".TRUE." if value else ".FALSE."
        else: 
            return str(value)


