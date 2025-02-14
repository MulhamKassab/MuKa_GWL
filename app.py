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
from NFL_COF_1and2Sided import find_load_for_given_length
from cof_recommendation import find_correct_thickness

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/calculate", methods=['POST'])
def calculate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Extract the original data and plyThicknessList from the combined structure
    input_data = data.get('data', {})

    # Validate that input_data is a dictionary
    if not isinstance(input_data, dict):
        return jsonify({"error": "Invalid data format"}), 400

    modulus_of_elasticity = 71700000
    shortDurationLoad = input_data.get('shortDurationLoad', 0)
    longDurationLoad = input_data.get('longDurationLoad', 0)
    allowable_Deflection = input_data.get('allowable_Deflection', 0)
    glass_length = input_data.get('glassLength', 0)
    glass_width = input_data.get('glassWidth', 0)
    number_of_supported_sides = input_data.get('numberOfSupportedSides', 0)
    glazing_type = input_data.get('glazingType', 0)
    number_of_layers = input_data.get('numberOfLayers', 0)
    layers_types = input_data.get('layersTypes', [])
    layers_thicknesses = input_data.get('layersThicknesses', [])
    plyThicknessList = data.get('plyThicknessList', [])
    glass_layers_strength_type = input_data.get('glassLayersStrengthType', [])
    number_of_plies = input_data.get('numberOfPlies', 0)
    pvb_thicknesses = input_data.get('pvbThicknesses', [])  # Retrieve the PVB thicknesses sent from JS
    interlayerTypes = input_data.get('interlayerTypes', [])
    airGap = input_data.get('airGap', 0)
    first_page_image_path = "download/first_page.jpg"

    nfl_result = []
    gtf = get_gtf_value(glass_layers_strength_type, glazing_type)
    short_cof_to_send = []
    long_cof_to_send = []
    lr = []
    lr_value = 0
    recommended_thickness = {'Short': [], 'Long': []}
    # Generate plot and save as image
    temp__dir = os.path.join(os.getcwd(), "download")
    os.makedirs(temp__dir, exist_ok=True)
    logo_path = os.path.join(temp__dir, "logo.png")
    first_page_image_path = os.path.join(temp__dir, "first_page.jpg")

    # Perform NFL calculation for each layer's thickness
    if number_of_supported_sides == 4:
        for thickness in layers_thicknesses:
            try:
                result = calculate_nfl(glass_length, glass_width, number_of_supported_sides, thickness, layers_types)

            except:
                return jsonify("Adjust your input data"), 400

            if isinstance(result, tuple):
                NFL_interpolated, jsonX, jsonY, jsonNFL, length, width, xi, yi, zi, AR, key = result
                nfl_result.append(round(float(NFL_interpolated), 2))  # Convert to float
            else:
                return result
            try:
                cof_short_duration = round(
                    float(calculate_cof(shortDurationLoad, glass_length, glass_width, modulus_of_elasticity, thickness,
                                        interlayerTypes)), 2)

                short_cof_to_send.append(cof_short_duration)

                if longDurationLoad != 0:
                    cof_long_duration = round(
                        float(calculate_cof(longDurationLoad, glass_length, glass_width, modulus_of_elasticity,
                                            thickness, interlayerTypes)), 2)
                    long_cof_to_send.append(cof_long_duration)
            except ValueError:
                if number_of_supported_sides == 4:
                    return jsonify("Adjust the width or the length of the glass"), 400
                else:
                    return jsonify("Adjust the length of the unsupported side"), 400

            except TypeError:
                if number_of_supported_sides == 4:
                    return jsonify("Adjust the widt or the length of the glass"), 400
                else:
                    return jsonify("Adjust the length of the unsupported side"), 400

        try:
            # calculated_nfl = nfl_result[0] if isinstance(nfl_result, list) and nfl_result else nfl_result
            calculated_nfl = nfl_result

            plot_interpolated_nfl = []
            for index, (layers_thickness, layer_type) in enumerate(zip(layers_thicknesses, layers_types)):
                interpolated_nfl, plot_paths = plot_nfl_from_json(
                    glass_length, glass_width, number_of_supported_sides,
                    layers_thickness, os.path.join(temp__dir, f"nfl_plot_{layers_thickness}"),
                    calculated_nfl, layer_type, index  # Pass the index along with other parameters
                )
                plot_interpolated_nfl.append(interpolated_nfl)

        except Exception as e:
            return jsonify("Adjust your input data"), 400

    else:
        try:
            for thickness, layer_type in zip(layers_thicknesses, layers_types):
                nfl_result.append(find_load_for_given_length(thickness, glass_length, layer_type,
                                                             number_of_supported_sides, "NFL", 0,
                                                             interlayerTypes))

                cof_short_duration = find_load_for_given_length(thickness, glass_length, layer_type,
                                                                number_of_supported_sides, "COF", shortDurationLoad,
                                                                interlayerTypes)
                short_cof_to_send.append(cof_short_duration)

                if longDurationLoad != 0:
                    cof_long_duration = find_load_for_given_length(thickness, glass_length, layer_type,
                                                                   number_of_supported_sides, "COF", longDurationLoad,
                                                                   interlayerTypes)
                    long_cof_to_send.append(cof_long_duration)
        except:
            return jsonify("Adjust your input data"), 400

    # Load share factor (LSF) and LR calculations
    if glazing_type == "double":
        try:
            lsf_value = get_load_share_factor(layers_thicknesses, layers_types)
        except:
            return jsonify("Adjust your input data"), 400

        try:
            if number_of_supported_sides == 4:
                lr_value = calculate_lr(plot_interpolated_nfl, gtf, lsf_value, glazing_type)
            else:
                lr_value = calculate_lr(nfl_result, gtf, lsf_value, glazing_type)
            lr.append(lr_value)
        except:
            return jsonify("Adjust your input data"), 400

    else:
        lsf_value = None  # or a more meaningful default value, if None isn't appropriate
        if number_of_supported_sides == 4:
            try:
                for nfl_interpolated_value in plot_interpolated_nfl:
                    lr_value = calculate_lr(nfl_interpolated_value, gtf, lsf_value, "single")
            except:
                return jsonify("Adjust your input data"), 400

        else:
            try:
                for nfl_value in nfl_result:
                    lr_value = calculate_lr(nfl_value, gtf, lsf_value, "single")
            except:
                return jsonify("Adjust your input data"), 400
        lr.append(lr_value)

    # Generate PDF in memory
    pdf_bytes = io.BytesIO()

    # Calculate glass weight including PVB layers
    try:
        glass_weight = calculate_glass_weight(
            glass_length, glass_width, layers_thicknesses, layers_types, pvb_thicknesses=pvb_thicknesses
        )
    except:
        return jsonify("Adjust your input data"), 400

    print("short_cof_to_send", short_cof_to_send)
    print("long_cof_to_send", long_cof_to_send)

    if short_cof_to_send[0] > float(allowable_Deflection) or (len(long_cof_to_send) > 0 and long_cof_to_send[0] >
                                                              float(allowable_Deflection)):

        recommended_thickness = find_correct_thickness(shortDurationLoad, longDurationLoad, allowable_Deflection,
                                                       number_of_supported_sides, glass_length, glass_width,
                                                       modulus_of_elasticity, interlayerTypes,
                                                       layer_type)
        print("recommended_thickness", recommended_thickness)

    create_pdf(pdf_bytes, glass_length, glass_width, pvb_thicknesses, number_of_supported_sides, layers_thicknesses,
               plyThicknessList, glass_weight, shortDurationLoad, longDurationLoad, allowable_Deflection, lr,
               glazing_type, short_cof_to_send, long_cof_to_send, layers_types, interlayerTypes, recommended_thickness,
               airGap, glass_layers_strength_type, logo_path, first_page_image_path)
    pdf_bytes.seek(0)

    # Save PDF to a temporary location
    temp_pdf_path = os.path.join(temp__dir, "deflection_result.pdf")
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
