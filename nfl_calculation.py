import os
import json
import numpy as np
from scipy.interpolate import griddata


def calculate_nfl(length, width, supported_sides, layer_thickness, layer_types):
    for layer_type in layer_types:
        key = f"NFL{layer_thickness}mm{supported_sides}S"
        json_file_path = os.path.join('.', 'Json', 'NFL', f'{layer_type}', f'{supported_sides}Sided', f"{key}.json")

        try:
            with open(json_file_path, 'r') as file:
                spec_data = json.load(file)
                if key in spec_data:
                    data_list = spec_data[key]
                    jsonNFL = np.array([item['NFL'] for item in data_list])
                    jsonX = np.array([item['X'] for item in data_list])
                    jsonY = np.array([item['Y'] for item in data_list])

                    AR = length / width  # Calculate AR
                    NFL_interpolated, xi, yi, zi = interpolate_nfl_griddata(length, width, AR, jsonX, jsonY, jsonNFL)

                    if np.isnan(NFL_interpolated):
                        return 0, jsonX, jsonY, jsonNFL, length, width, xi, yi, zi, AR, key

                    return NFL_interpolated, jsonX, jsonY, jsonNFL, length, width, xi, yi, zi, AR, key
                else:
                    return {"error": "Data not found for the given parameters"}, 404

        except FileNotFoundError as fnf_error:
            print(f"File not found error: {fnf_error}")
            return {"error": str(fnf_error)}, 404
        except (ValueError, KeyError) as e:
            print(f"Value error: {e}")
            return {"error": str(e)}, 400
        except Exception as e:
            print(f"General error: {e}")
            return {"error": str(e)}, 500


def interpolate_nfl_griddata(length, width, ar, json_x, json_y, json_nfl):
    if length < width:
        length, width = width, length
    #
    if length == width:
        length += 10
        points = np.array(list(zip(json_x, json_y)))
        NFL_interpolated = griddata(points, json_nfl, (length, width), method='cubic')
        xi = np.linspace(min(json_x), max(json_x), 100)
        yi = np.linspace(min(json_y), max(json_y), 100)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata(points, json_nfl, (xi, yi), method='nearest')

        return NFL_interpolated, xi, yi, zi
    else:
        points = np.array(list(zip(json_x, json_y)))
        NFL_interpolated = griddata(points, json_nfl, (length, width), method='cubic')
        xi = np.linspace(min(json_x), max(json_x), 100)
        yi = np.linspace(min(json_y), max(json_y), 100)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata(points, json_nfl, (xi, yi), method='cubic')

        return NFL_interpolated, xi, yi, zi
