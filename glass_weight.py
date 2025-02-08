import math

# Define the glass thickness and corresponding weight (in kg/m²) based on the first table
GLASS_WEIGHT_MAP = {
    2.5: 5.7,
    3.0: 7.6,
    4.0: 9.9,
    5.0: 11.9,
    6.0: 14.6,
    8.0: 19.5,
    10.0: 24.4,
    12.0: 31.2,
    16.0: 39.5,
    19.0: 47.8,
    20.0: 50.19
}

# Define the interlayer thickness and corresponding weight (in kg/m²) based on the second table
INTERLAYER_WEIGHT_MAP = {
    0.38: 0.40,
    0.76: 0.84,
    1.14: 1.20,
    1.52: 1.60,
    1.524: 1.6,
    2.29: 2.50
}


# Helper function to find the closest thickness in the weight map
def find_closest_value(thickness, weight_map):
    """
    Finds the closest available thickness from the weight map if the exact thickness is not found.

    Args:
        thickness (float): The thickness for which to find the closest match.
        weight_map (dict): The map containing thickness-weight pairs.

    Returns:
        float: The weight corresponding to the closest thickness.
    """
    # Find the closest thickness available in the map using absolute difference
    closest_thickness = min(weight_map.keys(), key=lambda x: abs(x - thickness))
    return weight_map[closest_thickness]


def calculate_glass_weight(glass_length, glass_width, layers_thickness, glass_types, pvb_thicknesses=None):
    """
    Calculate the total weight of the glass, including the interlayer weight for laminated glass.

    Args:
        glass_length (float): The length of the glass in mm.
        glass_width (float): The width of the glass in mm.
        layers_thickness (list): A list of thickness values (in mm) for each glass layer.
        glass_types (list): A list of types ('mono' or 'laminated') for each layer of glass.
        pvb_thicknesses (list, optional): A list of PVB (interlayer) thicknesses for laminated glass.

    Returns:
        float: The total calculated weight of the glass (in kg), rounded to two decimal places.
    """

    # Convert length and width from mm to meters to calculate the area in m²
    area = (glass_length / 1000) * (glass_width / 1000)
    total_weight = 0

    # Ensure pvb_thicknesses is not None, even if not provided
    if pvb_thicknesses is None:
        pvb_thicknesses = []

    # Iterate over each layer's thickness and glass type
    for i, (thickness, glass_type) in enumerate(zip(layers_thickness, glass_types)):
        # Check if the thickness is available in the GLASS_WEIGHT_MAP
        if thickness in GLASS_WEIGHT_MAP:
            weight_per_m2 = GLASS_WEIGHT_MAP[thickness]
        else:
            # If the thickness is not found, find the closest available thickness
            weight_per_m2 = find_closest_value(thickness, GLASS_WEIGHT_MAP)
            print(f"Thickness {thickness} mm not found in GLASS_WEIGHT_MAP. Using closest value.")

        # Calculate the weight of the glass layer based on area
        weight = weight_per_m2 * area
        total_weight += weight

        # If the glass is laminated and pvb_thicknesses are provided, calculate interlayer weight
        if glass_type == 'laminated' and i < len(pvb_thicknesses):
            pvb_thickness = pvb_thicknesses[i]
            if pvb_thickness in INTERLAYER_WEIGHT_MAP:
                interlayer_weight_per_m2 = INTERLAYER_WEIGHT_MAP[pvb_thickness]
            else:
                # If the PVB thickness is not found, find the closest available thickness
                interlayer_weight_per_m2 = find_closest_value(pvb_thickness, INTERLAYER_WEIGHT_MAP)
                print(f"PVB thickness {pvb_thickness} mm not found in INTERLAYER_WEIGHT_MAP. Using closest value.")

            # Calculate the interlayer (PVB) weight and add it to the total weight
            interlayer_weight = interlayer_weight_per_m2 * area
            total_weight += interlayer_weight

    # Return the total weight rounded to two decimal places
    return round(total_weight, 2)
