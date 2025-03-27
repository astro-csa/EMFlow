import subprocess
import shutil
from dataclasses import asdict, is_dataclass
from pathlib import Path

class EMSoftProgram:
    def __init__(self, name: str, config: object):
        self.name = name
        self.config = config

    def generate_config(self):
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

        result = subprocess.run(
            [executable, main_config_path.name],
            cwd=main_config_path.parent
        )

        if result.returncode == 0:
            print(f"[{self.name}] ✅ Execution completed.")
        else:
            print(f"[{self.name}] ❌ Execution failed with code {result.returncode}")


    def _generate_config_file(self, section: object) -> str:
        header = getattr(section, "header", None)
        filename = getattr(section, "filename", None)

        if not filename:
            return
        
        data = asdict(section)

        if header:
            lines = [f"&{header}"]
        else:
            lines = []
        
        for key, value in data.items():
            if key in ["header", "filename"]:
                continue
            if isinstance(value, str):
                lines.append(f" {key} = '{value}',")
            elif isinstance(value, bool):
                val_str = ".TRUE." if value else ".FALSE."
                lines.append(f" {key} = {val_str},")
            else:
                lines.append(f" {key} = {value},")
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
