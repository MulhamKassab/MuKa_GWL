import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.spatial import cKDTree
import json

# Set the Matplotlib backend to 'Agg' to avoid Tkinter issues
plt.switch_backend('Agg')


# Calculate the NFL value using distance-based interpolation


# Compute Catmull-Rom spline for smooth curve generation
def catmull_rom_spline(P0, P1, P2, P3, n_points=200):
    alpha = 0.5

    def tj(ti, Pi, Pj):
        return (np.linalg.norm(Pj - Pi)) ** alpha + ti

    t0 = 0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)

    if t1 == t0 or t2 == t1 or t3 == t2:
        return np.array([P1, P2])

    t = np.linspace(t1, t2, n_points)
    A1 = np.divide((t1 - t)[:, None] * P0 + (t - t0)[:, None] * P1, (t1 - t0), where=(t1 - t0) != 0)
    A2 = np.divide((t2 - t)[:, None] * P1 + (t - t1)[:, None] * P2, (t2 - t1), where=(t2 - t1) != 0)
    A3 = np.divide((t3 - t)[:, None] * P2 + (t - t2)[:, None] * P3, (t3 - t2), where=(t3 - t2) != 0)
    B1 = np.divide((t2 - t)[:, None] * A1 + (t - t0)[:, None] * A2, (t2 - t0), where=(t2 - t0) != 0)
    B2 = np.divide((t3 - t)[:, None] * A2 + (t - t1)[:, None] * A3, (t3 - t1), where=(t3 - t1) != 0)
    C = np.divide((t2 - t)[:, None] * B1 + (t - t1)[:, None] * B2, (t2 - t1), where=(t2 - t1) != 0)
    return C


# Plot the intersection points between the aspect ratio line and the NFL lines
def plot_intersection_points(ax, intersection_points):
    for ix, iy, nfl in intersection_points:
        ax.scatter([ix], [iy], color='green', s=10, zorder=5)
        ax.text(ix, iy, f'NFL={nfl}', fontsize=8, ha='left', color='green')


# Load data from the specified JSON file
def load_data(json_file_path, key):
    try:
        with open(json_file_path, 'r') as file:
            spec_data = json.load(file)
            if key not in spec_data:
                raise ValueError(f"Data not found for the given parameters: {key}")
            return spec_data[key]
    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
        raise fnf_error
    except (ValueError, KeyError) as e:
        print(f"Value error: {e}")
        raise e
    except Exception as e:
        print(f"General error: {e}")
        raise e


# Group points by their NFL values
def group_points_by_nfl(data_list):
    grouped_points = defaultdict(list)
    for point in data_list:
        grouped_points[point["NFL"]].append((point["X"], point["Y"]))
    return grouped_points


# Plot the NFL curves for the given data
def plot_nfl_curves(ax, grouped_points):
    all_points = []
    for nfl, points in grouped_points.items():
        coords = np.array(points)
        all_points.append(coords)

        if len(coords) < 4:
            ax.plot(coords[:, 0], coords[:, 1], color='black')
            ax.text(coords[0, 0], coords[0, 1], f'NFL={nfl}', fontsize=8, ha='right', color='black')
            continue

        extended_coords = np.vstack([coords[0], coords[0], coords, coords[-1], coords[-1]])
        curve_points = []
        for i in range(1, len(extended_coords) - 2):
            P0, P1, P2, P3 = extended_coords[i - 1], extended_coords[i], extended_coords[i + 1], extended_coords[i + 2]
            segment = catmull_rom_spline(P0, P1, P2, P3, n_points=100)
            curve_points.extend(segment)
        curve_points = np.array(curve_points)
        ax.plot(curve_points[:, 0], curve_points[:, 1], color='black')
        ax.text(curve_points[0, 0], curve_points[0, 1], f'NFL={nfl}', fontsize=8, ha='right', color='black')
    return all_points


def plot_top_diagonal_line(ax, grouped_points, extension_factor=10):
    # Identify the first NFL line
    first_nfl = sorted(grouped_points.keys())[-1]
    # Extract the first point from the first NFL line
    if grouped_points[first_nfl]:
        first_point = grouped_points[first_nfl][0]  # Get the first point
        # Calculate extended coordinates
        extended_x = first_point[0] * extension_factor
        extended_y = first_point[1] * extension_factor
        ax.plot([0, extended_x], [0, extended_y], 'k-')


def plot_bottom_diagonal_line(ax, grouped_points, extension_factor=10):
    # Identify the first NFL line
    last_nfl = sorted(grouped_points.keys())[-1]
    # Extract the first point from the first NFL line
    if grouped_points[last_nfl]:
        first_point = grouped_points[last_nfl][-1]  # Get the first point
        # Calculate extended coordinates
        extended_x = first_point[0] * extension_factor
        extended_y = first_point[1] * extension_factor
        ax.plot([0, extended_x], [0, extended_y], 'k-')


# Set the grid for the plot
# Set the grid for the plot using Matplotlib's built-in grid functions
def set_grid(ax, max_x, max_y):
    major_ticks_x = np.arange(0, max_x + 200, 1000)
    minor_ticks_x = np.arange(0, max_x + 200, 200)
    major_ticks_y = np.arange(0, max_y + 200, 1000)
    minor_ticks_y = np.arange(0, max_y + 200, 200)

    ax.set_xticks(major_ticks_x)
    ax.set_xticks(minor_ticks_x, minor=True)
    ax.set_yticks(major_ticks_y)
    ax.set_yticks(minor_ticks_y, minor=True)

    ax.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
    ax.grid(which='minor', color='gray', linestyle=':', linewidth=0.5)
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)


# Draw an aspect ratio line on the plot
def draw_aspect_ratio_line(length, width, extension_factor=1):
    extended_length = length * extension_factor
    extended_width = width * extension_factor
    plt.plot([0, extended_length], [0, extended_width], 'g--')


# Find the closest points to the given length and width
def find_closest_points(length, width, data_list, n_points=4):
    if width > length:
        width, length = length, width

    points = [(point["X"], point["Y"]) for point in data_list]
    if not points:
        return [], np.array([])

    tree = cKDTree(points)
    distances, indices = tree.query([[length, width]], k=min(n_points, len(points)))

    closest_points = [data_list[idx] for idx in indices[0] if idx < len(data_list)]
    closest_coords = np.array([points[idx] for idx in indices[0] if idx < len(data_list)])
    return closest_points, closest_coords


# Plot the closest points to the target point
def plot_closest_points(ax, closest_coords):
    ax.scatter(closest_coords[:, 0], closest_coords[:, 1], color='blue', s=5, zorder=5)


# Plot the target point on the graph
def plot_target_point(ax, length, width):
    ax.scatter([length], [width], color='black', s=10, zorder=5)
    ax.axvline(x=length, color='red', linestyle='--', linewidth=1)
    ax.axhline(y=width, color='red', linestyle='--', linewidth=1)


# Perform inverse distance weighting to estimate the NFL value at a point
def inverse_distance_weighting(x, y, points):
    weights = []
    epsilon = 1e-10
    for point in points:
        distance = np.sqrt((point['X'] - x) ** 2 + (point['Y'] - y) ** 2) + epsilon
        if distance == 0:
            return point['NFL']
        weights.append(1 / distance)

    weighted_nfl = sum(point['NFL'] * weight for point, weight in zip(points, weights)) / sum(weights)
    return float(weighted_nfl)


# Find the NFL lines that enclose the calculated NFL value
def find_enclosing_nfl_lines(calculated_nfl, grouped_points):
    nfl_values = sorted(grouped_points.keys())
    lower_nfl = None
    upper_nfl = None
    for nfl in nfl_values:
        if nfl <= calculated_nfl:
            lower_nfl = nfl
        if nfl > calculated_nfl:
            upper_nfl = nfl
            break
    return lower_nfl, upper_nfl


# Find intersection points between the aspect ratio line and the NFL lines
def find_intersection_points(length, width, grouped_points, lower_nfl, upper_nfl):
    intersection_points = []
    for nfl in [lower_nfl, upper_nfl]:
        points = np.array(grouped_points[nfl])
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            if (p1[1] - p1[0] * width / length) * (p2[1] - p2[0] * width / length) <= 0:
                t = (p1[1] - p1[0] * width / length) / (
                        (p1[1] - p1[0] * width / length) - (p2[1] - p2[0] * width / length))
                intersection_x = p1[0] + t * (p2[0] - p1[0])
                intersection_y = p1[1] + t * (p2[1] - p1[1])
                intersection_points.append((intersection_x, intersection_y, nfl))
                break
    return intersection_points


# Find and weight the closest points from the NFL lines
def find_and_weight_closest_points_from_nfl_lines(length, width, grouped_points, lower_nfl, upper_nfl, n_points=4,
                                                  ax=None):
    n_points_per_line = max(1, n_points // 2)

    lower_points = [{"X": x, "Y": y, "NFL": lower_nfl} for x, y in grouped_points[lower_nfl]]
    closest_lower_points, closest_lower_coords = find_closest_points(length, width, lower_points, n_points_per_line)

    upper_points = [{"X": x, "Y": y, "NFL": upper_nfl} for x, y in grouped_points[upper_nfl]]
    closest_upper_points, closest_upper_coords = find_closest_points(length, width, upper_points, n_points_per_line)

    combined_points = closest_lower_points + closest_upper_points
    combined_coords = np.vstack([closest_lower_coords, closest_upper_coords])

    # if ax is not None:
    #     ax.scatter(combined_coords[:, 0], combined_coords[:, 1], color='purple', s=5, zorder=5)

    weighted_nfl = inverse_distance_weighting(length, width, combined_points)
    return weighted_nfl


# Main function to plot NFL from JSON data
def plot_nfl_from_json(length, width, supported_sides, layer_thickness, save_path, calculated_nfl, layer_type, index):
    weighted_nfl_from_nfl_lines = []
    plot_image_paths = []
    key = f"NFL{layer_thickness}mm{supported_sides}S"
    json_file_path = os.path.join('.', 'Json', 'NFL', f'{layer_type}', f'{supported_sides}Sided', f"{key}.json")

    if width > length:
        width, length = length, width

    data_list = load_data(json_file_path, key)
    grouped_points = group_points_by_nfl(data_list)

    fig, ax = plt.subplots()
    all_points = plot_nfl_curves(ax, grouped_points)
    # max_x = max(all_points, key=lambda p: p[:, 0].max())[0].max()
    # max_y = max(all_points, key=lambda p: p[:, 1].max())[1].max()
    # Combine all points to determine the plotting range
    all_points = np.vstack(all_points)
    max_x = all_points[:, 0].max()
    max_y = all_points[:, 1].max()

    plot_top_diagonal_line(ax, grouped_points)
    plot_bottom_diagonal_line(ax, grouped_points)
    set_grid(ax, max_x, max_y)
    draw_aspect_ratio_line(length, width)

    n_points = 3
    n_points += 1
    closest_points, closest_coords = find_closest_points(length, width, data_list, n_points)
    # plot_closest_points(ax, closest_coords)
    plot_target_point(ax, length, width)

    lower_nfl, upper_nfl = find_enclosing_nfl_lines(calculated_nfl[index], grouped_points)
    # intersection_points = find_intersection_points(length, width, grouped_points, lower_nfl, upper_nfl)
    # plot_intersection_points(ax, intersection_points)

    n_points = 3
    n_points += 1
    weighted_nfl_from_nfl_lines.append(find_and_weight_closest_points_from_nfl_lines(length, width, grouped_points,
                                                                                     lower_nfl, upper_nfl, n_points,
                                                                                     ax=ax))

    ax.set_title(f'NFL for {layer_thickness} mm with {supported_sides} sided support', pad=20)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    current_plot_path = f"{save_path}_plot_{index + 1}.png"
    plt.savefig(current_plot_path)
    plt.close()

    plot_image_paths.append(current_plot_path)
    # print(f"math NFL = {calculated_nfl[index]}")
    # print("4 points NFL2 = ", weighted_nfl_from_nfl_lines)
    # print("weighted_nfl_from_nfl_lines", weighted_nfl_from_nfl_lines)

    # for i in range(len(weighted_nfl_from_nfl_lines)):
    #     weighted_nfl_from_nfl_lines[i] = round(weighted_nfl_from_nfl_lines[i], 2)

    return round(weighted_nfl_from_nfl_lines[0], 2), plot_image_paths
