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

    def _generate_config_file(self, section: object) -> str:
        header = getattr(section, "header", None)
        filename = getattr(section, "filename", None)

        if not header or not filename:
            return
        
        data = asdict(section)
        lines = [f"&{header}"]
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
        output_path.write_text("\n".join(lines))
        print(f"[{self.name}] {output_path} generated.")
