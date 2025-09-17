import shutil
import subprocess
from dataclasses import asdict, is_dataclass

from ui.utils.config_context import ConfigContext


class EMSoftProgram:
    """
    Abstract base class for managing and executing EMSoft programs.

    This class defines shared logic and utility methods that are common across all EMSoft program wrappers.
    Subclasses are expected to implement or inherit the following:
    - `generate_config()`: To generate all necessary configuration (.nml/.json) files for the program.
    - `run()`: Optionally execute the program using the generated configuration files.

    Attributes:
        - name (str): The name of the program, which maps to the executable.
        - config (object): Dataclass containing the configuration parameters for the program.
        - copy_output_from (str | None): Specifies the source program to copy output files from, if required.
        - update_input_name (bool): Determines if input names need to be updated based on specific use cases.
    """

    def __init__(self, name: str, config: object):
        """
        Initialize the program wrapper with its name and configuration dataclass.

        Args:
            name (str): The name of the program (e.g., the executable name).
            config (object): A dataclass containing configuration parameters for the program.
        """
        self.name = name
        self.config = config
        self.copy_output_from = None
        self.update_input_name = False

    def generate_config(self):
        """
        Generate the necessary configuration files for the program based on its dataclass configuration.

        Iterates through the attributes of the configuration dataclass and generates the appropriate
        configuration files by calling `_generate_config_file()` for nested dataclasses.

        Raises:
            RuntimeError: If the configuration dataclass is improperly defined or missing fields.
        """
        for attr_name in self.config.__dataclass_fields__:  # Loop through fields in the dataclass
            attr = getattr(self.config, attr_name)  # Get the value of the field
            if is_dataclass(attr):  # If the field is itself a dataclass
                self._generate_config_file(attr)  # Generate a config file for this nested dataclass

    def copy_output_file(self, source_program: "EMSoftProgram", new_name: str | None = None) -> None:
        """
        Copy the output file from one EMSoft program to another, renaming it if needed.

        Args:
            source_program (EMSoftProgram): The source program from which to copy the output file.
            new_name (str | None): A new name for the output file (optional).

        Raises:
            RuntimeError: If the source program's output file cannot be found.
        """
        # Define the path to the folder where temporary files are stored
        temp_folder = ConfigContext.get_data_path() / "EMFlow" / "temp"

        # Construct the path to the source program's output file
        original_name = f"{source_program.name}.h5"
        source_path = temp_folder / source_program.name / original_name

        # Define the target directory for the current program
        target_dir = temp_folder / self.name
        target_dir.mkdir(parents=True, exist_ok=True)  # Ensure the target directory exists

        # Determine the target file name (use new name if provided, otherwise use the original name)
        target_filename = f"{new_name}.h5" if new_name else original_name
        target_path = target_dir / target_filename

        # Copy the source file to the target directory
        shutil.copy2(source_path, target_path)
        print(f"[{self.name}] Copied {original_name} from {source_program.name}/ as {target_filename}")

    def run(self):
        """
        Execute the program using the generated configuration file.

        Checks for the existence of the main configuration file and runs the program executable
        in the temporary folder. Captures and prints both stdout and stderr line-by-line.

        Handles errors and ensures proper reporting of the program's return status.

        Raises:
            FileNotFoundError: If the main configuration file is missing.
        """
        executable = self.name  # The program name as the executable command
        # Path to the main configuration file for this program
        main_config_path = ConfigContext.get_data_path() / "EMFlow" / "temp" / self.name / f"{self.name}.nml"

        # Check if the configuration file exists
        if not main_config_path.exists():
            print(f"[{self.name}] ❌ Config file not found: {main_config_path}")
            return

        print(f"[{self.name}] ▶️ Running: {executable} {main_config_path}")

        # Execute the program using subprocess.Popen
        process = subprocess.Popen(
            [executable, main_config_path.name],  # Command to run
            cwd=main_config_path.parent,  # Set the working directory
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            text=True,  # Decode the output to strings (instead of bytes)
            bufsize=1,  # Enable line-buffering
        )

        # Stream output line by line from stdout
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break  # Exit loop once the process has completed
            if output:
                print(f"[{self.name}] [STDOUT]: {output.strip()}")  # Print each line from stdout

        # Capture and print any remaining stderr output
        error_output = process.stderr.read()
        if error_output:
            print(f"[{self.name}] [STDERR]: {error_output.strip()}")  # Print stderr if there is any

        # Check the return code of the process
        if process.returncode == 0:
            print(f"[{self.name}] ✅ Execution completed.")  # Success
        else:
            print(f"[{self.name}] ❌ Execution failed with code {process.returncode}")  # Failure

    def _generate_config_file(self, section):
        """
        Generate a configuration file for a given section of the program configuration.

        Args:
            section (object): A dataclass section containing the configuration details.

        Raises:
            RuntimeError: If required attributes (e.g., filename) are missing in the section.
        """
        # Extract metadata from the section
        header = getattr(section, "header", None)
        filename = getattr(section, "filename", None)
        no_quote_fields = getattr(section, "no_quote_fields", [])

        if not filename:
            return  # Do nothing if no filename is specified

        # Convert the section into a dictionary if it's a dataclass
        if is_dataclass(section):
            data = asdict(section)

        # Start building the configuration file content
        if header:
            lines = [f"&{header}"]  # Add header if defined
        else:
            lines = []

        # Special handling for "euler.txt" if applicable
        if filename.lower() == "euler.txt":
            for key, value in data.items():
                if key in ["header", "filename", "no_quote_fields"]:
                    continue  # Skip metadata fields
                lines.append(f"{value}")  # Add each value directly to the file content

        else:
            # Generate configuration lines for other file types
            for key, value in data.items():
                if key in ["header", "filename", "no_quote_fields"]:
                    continue  # Skip metadata fields
                formatted = self._format_value(key, value, no_quote_fields)
                lines.append(f" {key} = {formatted},")
            lines.append("/")  # End the configuration block

        # Write the generated content to the configuration file
        data_path = ConfigContext.get_data_path()  # Get the base data path
        output_dir = data_path / "EMFlow" / "temp" / self.name  # Define the output directory
        output_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        output_path = output_dir / filename  # Define the full path to the output file
        output_path.write_text("\n".join(lines) + "\n")  # Write the content to the file
        print(f"[{self.name}] {output_path} generated.")  # Notify file generation

    def _format_value(self, key, value, no_quote_fields):
        """
        Format a configuration value for inclusion in a configuration file.

        Args:
            key (str): The key associated with the value.
            value (any): The value to be formatted.
            no_quote_fields (list): List of fields that should not have quotes around their values.

        Returns:
            str: The formatted configuration value as a string.
        """
        if isinstance(value, str):
            if key in no_quote_fields:  # Do not quote fields in the no_quote_fields list
                return value
            else:
                return f"'{value}'"  # Quote string values
        elif isinstance(value, bool):  # Format boolean values
            return ".TRUE." if value else ".FALSE."
        else:
            return str(value)  # Convert other types to string
