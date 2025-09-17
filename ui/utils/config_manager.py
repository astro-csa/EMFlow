import json
import os
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog

# Define the directory where configuration files for the program are stored
CONFIG_DIR = Path.home() / ".config/EMsoft"

# Define the specific configuration file name within the CONFIG_DIR
CONFIG_FILE = CONFIG_DIR / "EMFlow.json"


def get_data_path() -> Path:
    """
    This function attempts to determine the path to the required data directory for the program.
    It does so by checking multiple sources in the following order:
        1. Environment variable `EMSOFT_DATA_PATH`
        2. A previously saved configuration file
        3. User input through a dialog box (if the first two are unavailable)
    """
    # Check if the environment variable `EMSOFT_DATA_PATH` is set
    env_path = os.getenv("EMSOFT_DATA_PATH")
    if env_path:
        print(f"EMsoft environment data path: {env_path}")
        return Path(env_path)  # Return the path from the environment variable

    # If no environment variable, check for the configuration file
    if CONFIG_FILE.exists():
        # Open the configuration file and load it as JSON
        with open(CONFIG_FILE) as f:
            config = json.load(f)

        # Get the "data_path" value from the JSON file, defaulting to an empty string if not defined
        config_path = Path(config.get("data_path", ""))
        print(f"EMsoft config file data path: {config_path}")
        return config_path  # Return the path from the configuration file

    # If neither the environment variable nor the configuration file provides a path,
    # prompt the user to manually select the directory
    user_input = QFileDialog.getExistingDirectory(None, "Select EMsoft data folder")

    # If the user cancels the selection and no path is provided
    if not user_input:
        raise RuntimeError("Data folder not selected")  # Raise an error since the data path is critical

    # Convert the user-provided path to a Path object
    user_path = Path(user_input)

    # Ensure the configuration directory exists by creating it if necessary
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Save the user-provided path to the configuration file for future use
    with open(CONFIG_FILE, "w") as f:
        json.dump({"data_path": str(user_path)}, f, indent=4)

    print(f"EMsoft user data path: {user_path}")  # Notify the user of the path chosen
    return user_path  # Return the user-provided path
