from cof_calculation import calculate_cof
from NFL_COF_1and2Sided import find_load_for_given_length

thicknesses_4_sided = [2.5, 2.7, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0, 19.0, 22.0]
thicknesses_1_2_sided = [6, 8, 10, 12, 16, 19, 22]


def find_correct_thickness(shortDurationLoad, longDurationLoad, allowable_Deflection,
                           number_of_supported_sides, length, width,
                           modulus_of_elasticity, interlayerTypes, layer_type):

    thickness_to_send = {'Short': [], 'Long': []}
    # Choose the right list based on the number of supported sides
    if number_of_supported_sides == 4:
        thicknesses = thicknesses_4_sided
    else:
        thicknesses = thicknesses_1_2_sided

    # Short duration calculations
    for thickness in thicknesses:
        if number_of_supported_sides == 4:
            cof_short_duration = calculate_cof(shortDurationLoad, length, width, modulus_of_elasticity, thickness,
                                               interlayerTypes)
        else:
            cof_short_duration = find_load_for_given_length(thickness, length, layer_type,
                                                            number_of_supported_sides,
                                                            "COF", shortDurationLoad, interlayerTypes)

        if cof_short_duration <= allowable_Deflection:
            thickness_to_send['Short'].append(thickness)
            break  # Stop once a suitable thickness is found

    # Long duration calculations, only if a longDurationLoad is defined
    if longDurationLoad != 0:
        for thickness in thicknesses:
            if number_of_supported_sides == 4:
                cof_long_duration = calculate_cof(longDurationLoad, length, width, modulus_of_elasticity, thickness,
                                                  interlayerTypes)
            else:
                cof_long_duration = find_load_for_given_length(thickness, length, layer_type, number_of_supported_sides,
                                                               "COF", longDurationLoad, interlayerTypes)

            if cof_long_duration <= allowable_Deflection:
                thickness_to_send['Long'].append(thickness)
                break  # Stop once a suitable thickness is found
    return thickness_to_send


# Example call to the function
# result = find_correct_thickness(1.5, 2, 3, 4, 1500, 1000, 71700000, ["PVB"], "mono")
# print(result)
