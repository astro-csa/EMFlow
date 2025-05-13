from pathlib import Path
from gui.utils.config_manager import get_data_path

class ConfigContext:
    _data_path: Path | None = None
    _execution_timestamp: str | None = None

    @classmethod
    def set_data_path(cls, path: Path):
        cls._data_path = path

    @classmethod
    def get_data_path(cls) -> Path:
        if cls._data_path is None:
            raise RuntimeError("Data path has not been set.")
        return cls._data_path

    @classmethod
    def set_execution_timestamp(cls, timestamp: str):
        cls._execution_timestamp = timestamp

    @classmethod
    def get_execution_timestamp(cls) -> str:
        if cls._execution_timestamp is None:
            raise RuntimeError("Execution timestamp has not been set.")
        return cls._execution_timestamp
    
    @classmethod
    def get_timestamped_folder(cls) -> Path:
        if cls._data_path is None:
            raise RuntimeError("Data path has not been set.")
        if cls._execution_timestamp is None:
            raise RuntimeError("Execution timestamp has not been set.")
        return cls._data_path / "EMFlow" / cls._execution_timestamp