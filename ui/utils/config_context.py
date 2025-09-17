from pathlib import Path


class ConfigContext:
    """
    A class to manage configuration context during the program's runtime.
    It provides functionality to store and retrieve:
        1. The data path where required binaries or data files are located.
        2. An execution timestamp, used to uniquely identify the current execution session.
    """

    # Class-level attribute to store the data path, initially set to None
    _data_path: Path | None = None

    # Class-level attribute to store the execution timestamp, initially set to None
    _execution_timestamp: str | None = None

    @classmethod
    def set_data_path(cls, path: Path):
        """
        Sets the data path for the context.

        Args:
            path (Path): The file system path to the required data directory.
        """
        cls._data_path = path

    @classmethod
    def get_data_path(cls) -> Path:
        """
        Retrieves the data path for the context. If no path has been set, raises an exception.

        Returns:
            Path: The file system path to the required data directory.

        Raises:
            RuntimeError: If the data path has not been set.
        """
        if cls._data_path is None:
            raise RuntimeError("Data path has not been set.")  # Ensure the data path is set before accessing it
        return cls._data_path  # Return the stored data path

    @classmethod
    def set_execution_timestamp(cls, timestamp: str):
        """
        Sets the execution timestamp for the context.

        Args:
            timestamp (str): A string representing the unique timestamp of the current execution session.
        """
        cls._execution_timestamp = timestamp

    @classmethod
    def get_execution_timestamp(cls) -> str:
        """
        Retrieves the execution timestamp for the context. If no timestamp has been set, raises an exception.

        Returns:
            str: The string representation of the execution timestamp.

        Raises:
            RuntimeError: If the execution timestamp has not been set.
        """
        if cls._execution_timestamp is None:
            raise RuntimeError("Execution timestamp has not been set.")  # Ensure the timestamp is set before accessing it
        return cls._execution_timestamp  # Return the stored execution timestamp

    @classmethod
    def get_timestamped_folder(cls) -> Path:
        """
        Generates a path to a timestamped folder inside the data directory.
        This is used to store or organize files specific to the current execution session.

        Returns:
            Path: The file system path to the timestamped folder.

        Raises:
            RuntimeError: If either the data path or the execution timestamp has not been set.
        """
        if cls._data_path is None:
            raise RuntimeError("Data path has not been set.")  # Ensure the data path is set
        if cls._execution_timestamp is None:
            raise RuntimeError("Execution timestamp has not been set.")  # Ensure the timestamp is set
        return cls._data_path / "EMFlow" / cls._execution_timestamp  # Return the path to a timestamped folder
