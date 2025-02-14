import csv
import numbers
from cof_calculation import calculate_cof
from NFL_COF_1and2Sided import find_load_for_given_length

# Constants and variables setup
number_of_supported_sides = [1, 2, 4]
shortDurationLoads = [1, 1.5, 2]
allowable_Deflection = 19
layers_types = ["mono", "laminated"]
thicknesses_4_sided = [2.5, 2.7, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0, 19.0, 22.0]
thicknesses_1_2_sided = [6, 8, 10, 12, 16, 19, 22]
pvb_thicknesses = [1.52]
glass_layers_strength_type = ["tempered"]
modulus_of_elasticity = 71700000
interlayerTypes = ["PVB"]
counter = 0

# Open a CSV file to record results
with open('cof_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header to the CSV file
    writer.writerow(['Supported Sides', 'Load', 'Length', 'Width', 'Layer Type', 'Thickness', 'COF Value'])

    # Iterate over configurations
    for i in number_of_supported_sides:
        if i == 1:
            glass_lengths = [j for j in range(1000, 2500, 500)]
            layers_thicknesses = thicknesses_1_2_sided
            for shortDurationLoad in shortDurationLoads:
                for glass_length in glass_lengths:
                    for layer_type in layers_types:
                        for layers_thickness in layers_thicknesses:
                            cof_short_duration = find_load_for_given_length(layers_thickness, glass_length, layer_type,
                                                                            i, "COF", shortDurationLoad,
                                                                            interlayerTypes)
                            if isinstance(cof_short_duration, numbers.Number) and cof_short_duration < 50:
                                writer.writerow([i, shortDurationLoad, glass_length, 'N/A', layer_type,
                                                 layers_thickness, cof_short_duration])
                                counter += 1

        elif i == 2:
            glass_lengths = [j for j in range(1000, 3500, 500)]
            glass_widths = [k for k in range(1000, 1200, 500)]
            layers_thicknesses = thicknesses_1_2_sided
            for shortDurationLoad in shortDurationLoads:
                for glass_length in glass_lengths:
                    for glass_width in glass_widths:
                        for layer_type in layers_types:
                            for layers_thickness in layers_thicknesses:
                                cof_short_duration = find_load_for_given_length(layers_thickness, glass_length,
                                                                                layer_type, i, "COF", shortDurationLoad,
                                                                                interlayerTypes)
                                if isinstance(cof_short_duration, numbers.Number) and cof_short_duration < 50:
                                    writer.writerow([i, shortDurationLoad, glass_length, glass_width, layer_type,
                                                     layers_thickness, cof_short_duration])
                                    counter += 1

        elif i == 4:
            tested = []
            glass_lengths = [j for j in range(1000, 4500, 500)]
            glass_widths = [k for k in range(700, 2500, 500)]
            layers_thicknesses = thicknesses_4_sided
            for shortDurationLoad in shortDurationLoads:
                for glass_length in glass_lengths:
                    for glass_width in glass_widths:
                        for layer_type in layers_types:
                            for layers_thickness in layers_thicknesses:
                                try:
                                    if not (glass_length, glass_width, layers_thickness) in tested:
                                        tested.append((glass_length, glass_width,layers_thickness))
                                        cof_short_duration = calculate_cof(shortDurationLoad, glass_length, glass_width,
                                                                           modulus_of_elasticity,layers_thickness,
                                                                           layer_type)
                                        cof_short_duration = round(float(cof_short_duration), 2)
                                        if isinstance(cof_short_duration, numbers.Number) and cof_short_duration < 50:
                                            writer.writerow([i, shortDurationLoad, glass_length, glass_width,
                                                             layer_type, layers_thickness, cof_short_duration])
                                            counter += 1
                                except Exception as e:
                                    print(f"Error for load {shortDurationLoad}, length {glass_length}, width {glass_width}: {str(e)}")
                                    continue  # Continue to the next iteration

print(f"Total calculations: {counter}")
