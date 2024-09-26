import os
import json


def get_gtf_value(glass_layers_strength_type, glazing_type):
    """
    Retrieve the Glass Type Factor (GTF) values for both short and long load durations
    based on the strength type of the glass layers and the type of glazing (single or double).

    Args:
        glass_layers_strength_type (list): List of glass layer strength types (e.g., 'annealed', 'heatStrengthened').
        glazing_type (str): Type of glazing ('single' or 'double').

    Returns:
        dict: A dictionary containing the GTF values for both short and long durations.
              Example format: {'short': [GTF1, GTF2], 'long': [GTF1, GTF2]}
    """

    # Initialize dictionary to hold GTF values for short and long durations
    glass_layers_strength_type_array = {
        'short': [],
        'long': []
    }

    try:
        if glazing_type == 'single':
            # If glazing type is single, load GTF for single glazing
            json_file_path = os.path.join("./Json/GTF/GTF_SL.json")  # Path to the GTF JSON file for single glazing
            with open(json_file_path, 'r') as file:
                spec_data = json.load(file)

                # Extract short and long GTF values from the JSON file
                gtf_short_load_values = spec_data["GTF_Single_Lite"]["short"]
                gtf_long_load_values = spec_data["GTF_Single_Lite"]["long"]

                # Loop through the provided glass layer strength types and fetch the corresponding GTF values
                for glassLayerStrengthType in glass_layers_strength_type:
                    if glassLayerStrengthType in gtf_short_load_values and glassLayerStrengthType in gtf_long_load_values:
                        # Append short and long GTF values for each strength type to the respective lists
                        glass_layers_strength_type_array['short'].append(gtf_short_load_values[glassLayerStrengthType])
                        glass_layers_strength_type_array['long'].append(gtf_long_load_values[glassLayerStrengthType])
                    else:
                        raise ValueError(f"Invalid glass layer strength type: {glassLayerStrengthType}")

        elif glazing_type == 'double':
            # If glazing type is double, load GTF for double glazing
            json_file_path_short = os.path.join("./Json/GTF/GTF_IG_SD.json")  # Path to short duration GTF data
            json_file_path_long = os.path.join("./Json/GTF/GTF_IG_LD.json")  # Path to long duration GTF data

            # Open both short and long duration GTF data files
            with open(json_file_path_short, 'r') as file_short, open(json_file_path_long, 'r') as file_long:
                spec_data_short = json.load(file_short)["GTF"]
                spec_data_long = json.load(file_long)["GTF"]

                # For double glazing, expect two layers of glass
                if len(glass_layers_strength_type) == 2:
                    lite_1 = glass_layers_strength_type[0]  # First layer strength type
                    lite_2 = glass_layers_strength_type[1]  # Second layer strength type

                    # Fetch the GTF1 and GTF2 values for short duration
                    short_gtf_value = {
                        "GTF1": spec_data_short[lite_1][lite_2]["GTF1"],
                        "GTF2": spec_data_short[lite_1][lite_2]["GTF2"]
                    }

                    # Fetch the GTF1 and GTF2 values for long duration
                    long_gtf_value = {
                        "GTF1": spec_data_long[lite_1][lite_2]["GTF1"],
                        "GTF2": spec_data_long[lite_1][lite_2]["GTF2"]
                    }

                    # Append GTF values to respective lists
                    glass_layers_strength_type_array['short'].append(short_gtf_value["GTF1"])
                    glass_layers_strength_type_array['short'].append(short_gtf_value["GTF2"])
                    glass_layers_strength_type_array['long'].append(long_gtf_value["GTF1"])
                    glass_layers_strength_type_array['long'].append(long_gtf_value["GTF2"])
                else:
                    raise ValueError("For double glazing, exactly two glass layers must be specified.")
        else:
            raise ValueError(f"Invalid glazing type: {glazing_type}")

    # Handle file not found errors
    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
        return None

    # Handle invalid values (e.g., invalid strength type)
    except ValueError as ve:
        print(f"Value error: {ve}")
        return None

    # Catch any other general errors
    except Exception as e:
        print(f"General error: {e}")
        return None

    # Return the GTF values for short and long durations
    return glass_layers_strength_type_array
