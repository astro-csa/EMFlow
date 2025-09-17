import json

from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class EMSoftConfig:
    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4)

    @classmethod
    def load(cls, path: Path) -> "EMSoftConfig":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

