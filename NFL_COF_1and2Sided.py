import math
import json
import os


def load_json_file(layer_type, supported_sides, nfl_or_cof, interlayerTypes, base_dir="./Json"):
    """
    Load a JSON file based on the given parameters.

    Args:
        layer_type (str): Either "mono" or "laminated".
        supported_sides (str): Number of supported sides, usually "1" or "2".
        nfl_or_cof (str): Indicates whether to load NFL or COF data.
        base_dir (str): Base directory where the JSON files are located.

    Returns:
        dict or str: The data dictionary inside the top-level key, or an error message.
    """
    # Build the file path based on the parameters
    if nfl_or_cof == "NFL":
        file_path = os.path.join(
            base_dir,
            nfl_or_cof,
            layer_type,
            f"{nfl_or_cof}_{supported_sides}_{layer_type}.json"  # Example: 'NFL_1_mono.json'
        )
    elif nfl_or_cof == "COF":
        file_path = os.path.join(
            base_dir,
            nfl_or_cof,
            layer_type,
            f"{nfl_or_cof}_{supported_sides}_{layer_type}_{interlayerTypes[0]}.json"  # Example: 'NFL_1_mono_PVB.json'
        )



    try:
        # Load the JSON data from the file
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Return the dictionary inside the top-level key
        if nfl_or_cof == "NFL":
            top_level_key = f"{nfl_or_cof}_{supported_sides}_{layer_type}"
        else:
            top_level_key = f"{nfl_or_cof}_{supported_sides}_{layer_type}_{interlayerTypes[0]}"

        return data.get(top_level_key, f"Top-level key '{top_level_key}' not found in the JSON file.")

    except FileNotFoundError:
        return f"File not found: {file_path}"
    except json.JSONDecodeError:
        return "Error decoding JSON file."


def find_load_for_given_length(thickness, length, layer_type, supported_sides, nfl_or_cof, load, interlayerTypes):
    """
    Calculate the load or deflection based on given parameters using data from a JSON file.

    Args:
        thickness (int): Glass thickness.
        length (float): Length of the glass in mm.
        layer_type (str): Either "mono" or "laminated".
        supported_sides (str): Number of supported sides, usually "1" or "2".
        nfl_or_cof (str): Indicates whether to load NFL or COF data.
        load (float): The load to be applied.

    Returns:
        float or str: Calculated load or deflection, or an error message.
    """
    # Load the correct JSON data
    points_dict = load_json_file(layer_type, supported_sides, nfl_or_cof, interlayerTypes)

    # Check if the data is loaded correctly
    if isinstance(points_dict, str):
        return points_dict  # Return the error message

    if thickness > 19:
        thickness = 19
    # Check if the thickness exists in the points_dict
    points = points_dict.get(str(thickness))
    if not points or len(points) != 2:
        return "Invalid data or number of points for interpolation."

    # Extract points (x1, y1) and (x2, y2)
    (x1, y1), (x2, y2) = points

    try:
        if nfl_or_cof == "NFL":
            if y1 != y2:
                # Logarithmic interpolation for NFL
                x = x1 * (x2 / x1) ** (math.log(length / y1) / math.log(y2 / y1))
                return round(x, 5)
            else:
                return "Length values y1 and y2 cannot be the same."
        else:  # For COF calculation
            length_m = length / 1000  # Convert length from mm to meters
            length_m **= 4  # Raise length to the fourth power
            load_l4 = length_m * load

            # Log-log interpolation
            log_x1 = math.log10(x1)
            log_x2 = math.log10(x2)
            log_y1 = math.log10(y1)
            log_y2 = math.log10(y2)
            log_load_l4 = math.log10(load_l4)

            log_y = log_y1 + ((log_load_l4 - log_x1) / (log_x2 - log_x1)) * (log_y2 - log_y1)
            y = 10 ** log_y  # Convert back from logarithmic scale
            return round(y, 5)

    except ValueError as e:
        return f"Error in calculation: {str(e)}"


# Example usage:
if __name__ == "__main__":
    thickness = 12
    length = 1000  # Length in mm
    layer_type = "laminated"  # mono or laminated
    supported_sides = "1"  # 1 or 2
    nfl_or_cof = "NFL"  # NFL or COF
    load = 1  # Load value
    interlayerTypes = "SGP"

    result = find_load_for_given_length(thickness, length, layer_type, supported_sides, nfl_or_cof, load, interlayerTypes)
    print(result)