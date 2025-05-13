from pathlib import Path
import os
import json
from PyQt5.QtWidgets import QFileDialog

CONFIG_DIR = Path.home() / ".config/EMsoft"
CONFIG_FILE = CONFIG_DIR / "EMFlow.json"

def get_data_path() -> Path:
    # Environment variable
    env_path = os.getenv("EMSOFT_DATA_PATH")
    if env_path:
        print(f"EMsoft environment data path: {env_path}")
        return Path(env_path)
    
    # Configuration file
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        config_path = Path(config.get("data_path", ""))
        print(f"EMsoft config file data path: {config_path}")
        return config_path
    
    # User input
    user_input = QFileDialog.getExistingDirectory(None, "Select EMsoft data folder")

    if not user_input:
        raise RuntimeError("Data folder not selected")
    
    user_path = Path(user_input)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"data_path": str(user_path)}, f, indent=4)
    print(f"EMsoft user data path: {user_path}")
    return user_path
