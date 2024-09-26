import os
import io
from flask import Flask, jsonify, render_template, request, send_file, url_for
from nfl_calculation import calculate_nfl
from get_gtf import get_gtf_value
from lr_calculation import calculate_lr
from cof_calculation import calculate_cof
from pdf_creation import create_pdf
from newPlotting import plot_nfl_from_json
from glass_weight import calculate_glass_weight
from get_load_share_factor import get_load_share_factor

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/calculate", methods=['POST'])
def calculate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    modulus_of_elasticity = 71700000
    shortDurationLoad = data.get('shortDurationLoad', 0)
    longDurationLoad = data.get('longDurationLoad', 0)
    allowable_Deflection = data.get('allowable_Deflection', 0)
    glass_length = data.get('glassLength', 0)
    glass_width = data.get('glassWidth', 0)
    number_of_supported_sides = data.get('numberOfSupportedSides', 0)
    glazing_type = data.get('glazingType', 0)
    number_of_layers = data.get('numberOfLayers', 0)
    layers_types = data.get('layersTypes', [])
    layers_thicknesses = data.get('layersThicknesses', [])
    glass_layers_strength_type = data.get('glassLayersStrengthType', [])
    number_of_plies = data.get('numberOfPlies', 0)
    pvb_thicknesses = data.get('pvbThicknesses', [])  # Retrieve the PVB thicknesses sent from JS

    nfl_result = []
    gtf = get_gtf_value(glass_layers_strength_type, glazing_type)
    short_cof_to_send = []
    long_cof_to_send = []
    lr = []

    # Perform NFL calculation for each layer's thickness
    for thickness in layers_thicknesses:
        result = calculate_nfl(glass_length, glass_width, number_of_supported_sides, thickness, layers_types)
        if isinstance(result, tuple):
            NFL_interpolated, jsonX, jsonY, jsonNFL, length, width, xi, yi, zi, AR, key = result
            nfl_result.append(round(float(NFL_interpolated), 2))  # Convert to float
        else:
            return result

        cof_short_duration = round(
            float(calculate_cof(shortDurationLoad, glass_length, glass_width, modulus_of_elasticity, thickness)), 2)
        short_cof_to_send.append(cof_short_duration)

        cof_long_duration = round(
            float(calculate_cof(longDurationLoad, glass_length, glass_width, modulus_of_elasticity, thickness)), 2)
        long_cof_to_send.append(cof_long_duration)

    # Generate plot and save as image
    temp_plot_dir = os.path.join(os.getcwd(), "download")
    os.makedirs(temp_plot_dir, exist_ok=True)
    plot_image_path = os.path.join(temp_plot_dir, "nfl_plot.png")
    logo_path = os.path.join(temp_plot_dir, "logo.png")

    try:
        calculated_nfl = nfl_result[0] if isinstance(nfl_result, list) and nfl_result else nfl_result
        calculated_nfl = nfl_result

        plot_interpolated_nfl = []
        for index, (layers_thickness, layer_type) in enumerate(zip(layers_thicknesses, layers_types)):
            interpolated_nfl, plot_paths = plot_nfl_from_json(
                glass_length, glass_width, number_of_supported_sides,
                layers_thickness, os.path.join(temp_plot_dir, f"nfl_plot_{layers_thickness}"),
                calculated_nfl, layer_type, index  # Pass the index along with other parameters
            )
            plot_interpolated_nfl.append(interpolated_nfl)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Load share factor (LSF) and LR calculations
    if glazing_type == "double":
        lsf_value = get_load_share_factor(layers_thicknesses, layers_types)
        lr_value = calculate_lr(plot_interpolated_nfl, gtf, lsf_value, glazing_type)
        lr.append(lr_value)
    else:
        lsf_value = None  # or a more meaningful default value, if None isn't appropriate
        for nfl_interpolated_value in plot_interpolated_nfl:
            lr_value = calculate_lr(nfl_interpolated_value, gtf, lsf_value, "single")
            lr.append(lr_value)

    # Generate PDF in memory
    pdf_bytes = io.BytesIO()

    # Calculate glass weight including PVB layers
    glass_weight = calculate_glass_weight(
        glass_length, glass_width, layers_thicknesses, layers_types, pvb_thicknesses=pvb_thicknesses
    )

    create_pdf(pdf_bytes, glass_length, glass_width, number_of_supported_sides, layers_thicknesses, glass_weight,
               shortDurationLoad, longDurationLoad, allowable_Deflection, lr,
               short_cof_to_send, long_cof_to_send, layers_types,
               glass_layers_strength_type, logo_path)
    pdf_bytes.seek(0)

    # Save PDF to a temporary location
    temp_pdf_path = os.path.join(temp_plot_dir, "deflection_result.pdf")
    with open(temp_pdf_path, 'wb') as f:
        f.write(pdf_bytes.getbuffer())

    # Return the JSON response with a URL to download the PDF
    pdf_url = url_for('download_pdf', filename='deflection_result.pdf', _external=True)

    return jsonify({'pdf_url': pdf_url})


@app.route('/download/<filename>')
def download_pdf(filename):
    return send_file(os.path.join('download', filename))


if __name__ == '__main__':
    app.run(debug=True)
