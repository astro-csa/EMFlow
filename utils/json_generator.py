import json

def generate_foil_json(output_path):
    """
    Generates a JSON file with the fixed foil structure
    and saves it to the specified output path.

    Args:
        output_path (str): The file path to save the JSON file.
    """

    # Define the fixed structure of the foil JSON
    foil_data = {
        "FoilDescriptor": {
            "foilF": [0.0, 0.0, 1.0],
            "foilq": [1.0, 0.0, 0.0],
            "foilalP": 0.0,
            "foilalS": 0.0,
            "foilalR": 0.0,
            "foilz0": 100.0,
            "foilelmo": {
                "row1": [168.4, 121.4, 121.4, 0.0, 0.0, 0.0],
                "row2": [121.4, 168.4, 121.4, 0.0, 0.0, 0.0],
                "row3": [121.4, 121.4, 168.4, 0.0, 0.0, 0.0],
                "row4": [0.0, 0.0, 0.0, 75.5, 0.0, 0.0],
                "row5": [0.0, 0.0, 0.0, 0.0, 75.5, 0.0],
                "row6": [0.0, 0.0, 0.0, 0.0, 0.0, 75.5]
            }
        }
    }

    # Write the JSON data to the specified file
    try:
        with open(output_path, 'w') as json_file:
            json.dump(foil_data, json_file, indent=4)
        print(f"Foil JSON file successfully saved to: {output_path}")
    except Exception as e:
        print(f"Error saving foil JSON file: {e}")
