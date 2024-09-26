import json
import os

def get_load_share_factor(layer_thicknesses, layer_types):
    """
    Retrieve the load share factors (LS1, LS2) for given glass thicknesses from the appropriate JSON file.

    :param layer_thicknesses: List containing the thicknesses of the first and second glass layers (e.g., [2.5, 10])
    :param layer_types: List containing the layer types (e.g., ['mono', 'lami'])
    :return: A dictionary containing the load share factors for short and long duration [LS1, LS2]
    """
    if len(layer_thicknesses) != 2 or len(layer_types) != 2:
        raise ValueError("Both thicknesses and layers_types lists must contain exactly two elements.")

    first_layer_thickness, second_layer_thickness = map(str, layer_thicknesses)

    # Determine the correct JSON file based on layer types
    if layer_types == ['mono', 'lami']:
        short_duration_file = os.path.join("./Json/LSF", "LSF_DI.json")
        long_duration_file = os.path.join("./Json/LSF", "LSF_LongOnly.json")
    else:
        short_duration_file = long_duration_file = os.path.join("./Json/LSF", "LSF_DI.json")

    # Function to retrieve the LSF values from the given JSON file
    def load_lsf(json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)

        try:
            lsf_value = data["Load_Share_Factors"][first_layer_thickness][second_layer_thickness]
            return [lsf_value["LS1"], lsf_value["LS2"]]
        except KeyError:
            raise ValueError(f"No load share factor found for thicknesses: {first_layer_thickness} and {second_layer_thickness}")

    # Get LSF for both short and long duration
    lsf_short = load_lsf(short_duration_file)
    lsf_long = load_lsf(long_duration_file)

    return {
        "short_duration": lsf_short,
        "long_duration": lsf_long
    }