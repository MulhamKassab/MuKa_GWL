import os
import json
import math


def load_glass_thickness_data(json_file_path):
    """
    Load the glass thickness data from the JSON file.

    Parameters:
    - json_file_path (str): The path to the JSON file.

    Returns:
    - spec_data (dict): The JSON data containing glass thickness information.
    - None if the file is not found or an error occurs.
    """
    try:
        with open(json_file_path, 'r') as file:
            spec_data = json.load(file)
            return spec_data
    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
        return None
    except Exception as e:
        print(f"An error occurred while loading the JSON file: {e}")
        return None


def get_minimum_thickness(nominal_thickness, spec_data):
    """
    Retrieve the minimum glass thickness for the given nominal thickness from the spec_data.

    Parameters:
    - nominal_thickness (float): The nominal thickness of the glass.
    - spec_data (dict): The data containing nominal and minimum thickness mappings.

    Returns:
    - minimum_thickness (float): The minimum glass thickness if found.
    - None if no corresponding minimum thickness is found.
    """
    thickness = float(nominal_thickness)
    for glass in spec_data["Glass_Thicknesses"]:
        if float(glass["Nominal_mm"]) == thickness:
            return float(glass["Minimum_mm"])
    print(f"No corresponding minimum thickness found for nominal thickness {nominal_thickness}")
    return None


def calculate_x_value(literal_load, length, width, modulus_of_elasticity, thickness):
    """
    Calculate the logarithmic x-value used in the COF equation.

    Parameters:
    - literal_load (float): The literal load applied to the glass.
    - length (float): The length of the glass.
    - width (float): The width of the glass.
    - modulus_of_elasticity (float): The modulus of elasticity of the glass.
    - thickness (float): The minimum thickness of the glass.

    Returns:
    - x (float): The calculated x-value.
    """
    return math.log(math.log((literal_load * (length * width) ** 2) / (modulus_of_elasticity * thickness ** 4)))


def calculate_coefficients(length, width):
    """
    Calculate the coefficients (r0, r1, r2) based on the length-to-width ratio.

    Parameters:
    - length (float): The length of the glass.
    - width (float): The width of the glass.

    Returns:
    - r0, r1, r2 (tuple of floats): The calculated coefficients.
    """
    ratio = length / width
    r0 = 0.553 - 3.83 * ratio + 1.11 * ratio ** 2 - 0.0969 * ratio ** 3
    r1 = -2.29 + 5.83 * ratio - 2.17 * ratio ** 2 + 0.2067 * ratio ** 3
    r2 = 1.485 - 1.908 * ratio + 0.815 * ratio ** 2 - 0.0822 * ratio ** 3
    return r0, r1, r2


def calculate_center_of_deflection(r0, r1, r2, thickness, x):
    """
    Calculate the center of glass deflection (COF) based on the coefficients and x-value.

    Parameters:
    - r0, r1, r2 (float): The coefficients calculated using the length-to-width ratio.
    - thickness (float): The minimum thickness of the glass.
    - x (float): The logarithmic x-value calculated from the load and dimensions.

    Returns:
    - cof (float): The center of deflection (COF).
    """
    return thickness * math.exp(r0 + r1 * x + r2 * x ** 2)


def calculate_cof(literal_load, length, width, modulus_of_elasticity, nominal_thickness, interlayerTypes):
    """
    Main function to calculate the center of glass deflection (COF).

    Parameters:
    - literal_load (float): The literal load applied to the glass.
    - length (float): The length of the glass in mm.
    - width (float): The width of the glass in mm.
    - modulus_of_elasticity (float): The modulus of elasticity of the glass.
    - nominal_thickness (float): The nominal thickness of the glass in mm.

    Returns:
    - cof (float): The calculated center of glass deflection (COF) in mm.
    - None if an error occurs during processing.
    """

    # Load glass thickness data from JSON
    json_file_path = os.path.join("./Json/Glass_Thicknesses.json")
    spec_data = load_glass_thickness_data(json_file_path)
    if not spec_data:
        return None

    # Get minimum thickness corresponding to the nominal thickness
    minimum_thickness = get_minimum_thickness(nominal_thickness, spec_data)
    if minimum_thickness is None:
        return None

    # Calculate coefficients based on the length-to-width ratio
    r0, r1, r2 = calculate_coefficients(length, width)

    # Calculate the x-value for the COF equation
    if interlayerTypes == ["SGP"]:
        modulus_of_elasticity = 78000000
    x = calculate_x_value(literal_load, length, width, modulus_of_elasticity, minimum_thickness)
    # Calculate and return the center of deflection (COF)
    cof = calculate_center_of_deflection(r0, r1, r2, minimum_thickness, x)

    return cof

print(calculate_x_value(1.5, 1500, 1000, 71700000, 12))