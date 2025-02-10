const inputParams = {
    shortDurationLoad: 0,
    longDurationLoad: 0,
    allowable_Deflection: 0,
    glassLength: 0,
    glassWidth: 0,
    numberOfSupportedSides: 0,
    glazingType: 0,
    numberOfLayers: 0,
    layersTypes: [], // mono or lami
    layersThicknesses: [],
    glassLayersStrengthType: [],
    numberOfPlies: [],
    pvbThicknesses: [], // Array for PVB thicknesses
    interlayerTypes: []
};

function validateAndDownload() {
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    let allFilled = true;

    // Remove previous highlights and clear error messages
    requiredFields.forEach(field => {
        field.classList.remove('input-error');
    });

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; // Clear previous messages

    // Check for empty fields
    requiredFields.forEach(field => {
        if (field.value.trim() === '') {
            field.classList.add('input-error'); // Highlight empty fields
            allFilled = false;
        }
    });

    // Validate Short Duration Load is not zero
    const shortDurationLoadField = document.getElementById('ShortDurationLoad');
    const shortDurationLoad = parseFloat(shortDurationLoadField.value) || 0;

    if (shortDurationLoad <= 0) {
        shortDurationLoadField.classList.add('input-error'); // Highlight the field
        allFilled = false;

        const errorMessage = document.createElement('div');
        errorMessage.textContent = "Short Duration Load must be greater than zero.";
        errorMessage.style.color = "red";
        errorMessage.style.fontWeight = "bold";
        resultsDiv.appendChild(errorMessage);
    }

    if (allFilled) {
        gatherDataFromInput(); // Continue with the normal download process
    } else {
        const generalErrorMessage = document.createElement('div');
        generalErrorMessage.textContent = "Please correct the highlighted errors.";
        generalErrorMessage.style.color = "red";
        generalErrorMessage.style.fontWeight = "bold";
        resultsDiv.appendChild(generalErrorMessage);
    }
}


// Function to update input parameters
function setInputParameters(params) {
    Object.assign(inputParams, params);
    console.log("params = ", params);
}
function showSpinner() {
    document.getElementById('spinner').style.display = 'flex';
}

// Hide the spinner
function hideSpinner() {
    document.getElementById('spinner').style.display = 'none';
}

function gatherDataFromInput() {
    const shortDurationLoad = parseFloat(document.getElementById('ShortDurationLoad').value) || 0;
    const longDurationLoad = document.getElementById('LongDurationLoad').value.trim() === '' ? 0 : parseFloat(document.getElementById('LongDurationLoad').value);
    const allowable_Deflection = parseFloat(document.getElementById('Allowable_Deflection').value) || 0;
    const glassLength = parseFloat(document.getElementById('glassLength').value) || 0;
    const glassWidth = parseFloat(document.getElementById('glassWidth').value) || 0;
    const numberOfSupportedSides = parseInt(document.getElementById('numberOfSupportedSides').value) || 0;
    const glazingType = document.getElementById('glazingType').value;
    const numberOfLayers = glazingType === 'single' ? 1 : 2;
    // Check if the airGap input exists and is not empty, then parse it, otherwise set to 0
    let airGapInput = document.getElementById('airGap');
    let airGap = 0; // Default to 0
    if (airGapInput && airGapInput.value.trim() !== '') {
        airGap = parseFloat(airGapInput.value);
        if (isNaN(airGap)) { // Check if the parsed value is not a number
            airGap = 0; // Reset to 0 if the input value is not a valid number
            console.error('Invalid Air Gap value, defaulted to 0');
        }
    }


    inputParams.layersTypes = [];
    inputParams.layersThicknesses = [];
    inputParams.glassLayersStrengthType = [];
    inputParams.numberOfPlies = [];
    inputParams.pvbThicknesses = [];
    inputParams.interlayerTypes = [];
    const plyThicknessList = [];
    // Update inputParams with basic values
    setInputParameters({
        shortDurationLoad,
        longDurationLoad,
        allowable_Deflection,
        glassLength,
        glassWidth,
        numberOfSupportedSides,
        glazingType,
        numberOfLayers,
        layersTypes: [],
        layersThicknesses: [],
        glassLayersStrengthType: [],
        numberOfPlies: [],
        pvbThicknesses: [],
        interlayerTypes: [],
        airGap
    });

    // Loop through each layer
    for(let i = 0; i < numberOfLayers; i++) {
        const layerType = document.getElementById(`layerType${i}`).value;

        if(layerType === 'mono') {
            const layerThickness = parseFloat(document.getElementById(`monoThickness${i}`).value) || 0;
            inputParams.layersThicknesses.push(layerThickness);
            inputParams.layersTypes.push(layerType);

            const glassLayerStrengthType = document.getElementById(`monoType${i}`).value;
            inputParams.glassLayersStrengthType.push(glassLayerStrengthType);
            inputParams.numberOfPlies.push(1); // Single ply for monolithic layers
        } else if(layerType === 'laminated') {
            const numberOfPlies = parseInt(document.getElementById(`numPlys${i}`).value) || 0;
            inputParams.numberOfPlies.push(numberOfPlies);
            inputParams.layersTypes.push(layerType);

            let pliesTotalThickness = 0;

            const lami_1_2_sided_nominal = [5.56, 7.42, 9.02, 11.91, 15.09, 18.26,20];
            const lami_4_sided_nominal = [4.57,5.56, 7.42, 9.02, 11.91, 15.09, 18.26,20];

            const lami_1_2_sided = [6, 8, 10, 12, 16, 19,20];
            const lami_4_sided = [5, 6, 8, 10, 12, 16, 19,20];

            for(let j = 0; j < numberOfPlies; j++) {
                const plyThickness = parseFloat(document.getElementById(`plyThickness${i}-${j}`).value) || 0;
                pliesTotalThickness += plyThickness;
                plyThicknessList.push(plyThickness);
            }

            let totalPvbThicknesses = 0
            for(let k = 0; k < numberOfPlies - 1; k++) {
                const pvbThickness = parseFloat(document.getElementById(`interlayerThickness${i}-${k}`).value) || 0;
                const interlayerType = document.getElementById(`interlayerType${i}-${k}`).value; // New: Collect interlayer type
                inputParams.pvbThicknesses.push(pvbThickness); // Add the PVB/SGP thickness to the array
                inputParams.interlayerTypes.push(interlayerType);
                console.log(pvbThickness)
            }
            // Check if PVB thicknesses need to be included in combinedThickness
            let combinedThickness;
            let targetNominalList;
            let targetList;

            if (totalPvbThicknesses > 1.542) {
                // Include PVB thicknesses in combinedThickness and match with the nominal list
                combinedThickness = pliesTotalThickness + totalPvbThicknesses;
                console.log("Combined Thickness with PVB:", combinedThickness);

                // Use the nominal list for matching
                targetNominalList = numberOfSupportedSides < 4 ? lami_1_2_sided_nominal : lami_4_sided_nominal;
                targetList = numberOfSupportedSides < 4 ? lami_1_2_sided : lami_4_sided;
            } else {
                // Use only pliesTotalThickness and match directly with the normal list
                combinedThickness = pliesTotalThickness;
                console.log("Combined Thickness without PVB:", combinedThickness);

                // Use the normal list for matching
                targetList = numberOfSupportedSides < 4 ? lami_1_2_sided : lami_4_sided;
            }

            // Find the closest match
            const findClosest = (value, list) => {
                return list.reduce((a, b) => (Math.abs(b - value) * 0.7 < Math.abs(a - value) ? b : a));
            };

            let closestMatch;
            if (totalPvbThicknesses > 1.542) {
                // Match with the nominal list
                const closestIndex = targetNominalList.reduce((closestIndex, currentValue, currentIndex) => {
                    const closestValue = targetNominalList[closestIndex];
                    return Math.abs(currentValue - combinedThickness) < Math.abs(closestValue - combinedThickness)
                        ? currentIndex
                        : closestIndex;
                }, 0);
                closestMatch = targetList[closestIndex];
            } else {
                // Match directly with the normal list
                closestMatch = findClosest(combinedThickness, targetList);
            }

            // Push the results
            const laminatedLayerType = document.getElementById(`laminatedType${i}`).value;
            inputParams.glassLayersStrengthType.push(laminatedLayerType);
            inputParams.layersThicknesses.push(closestMatch);
            console.log("Closest Match:", closestMatch);

        }
    }
//    console.log("Updated inputParams: ", inputParams);
    // Show the spinner before sending the request
    showSpinner();
    sendToServer(inputParams, plyThicknessList);
}

// Function to send data to the server
function sendToServer(data, plyThicknessList) {
    const combinedData = { data, plyThicknessList };
    const jsonData = JSON.stringify(combinedData);
    console.log('jsonData = ', jsonData);

    axios.post('/calculate', jsonData, {
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        console.log('Server response:', response.data);
        const result = response.data;
        let resultText = 'Results:\n';

        // Display the formatted results
        document.getElementById('results').textContent = resultText;

        const pdfLink = document.createElement('a');
        pdfLink.href = result.pdf_url;
        pdfLink.textContent = 'Download results as PDF';
        pdfLink.target = '_blank';  // Open in a new tab

        const resultsDiv = document.getElementById('results');
        resultsDiv.appendChild(document.createElement('br'));
        resultsDiv.appendChild(pdfLink);
    })
    .catch(error => {
        console.error('Error sending data to the server:', error);

        // Extract the backend message and display it in the results div
        const errorMessage = error.response?.data || "An unexpected error occurred. Please try again.";
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `<div class="error-message">${errorMessage}</div>`; // Here is where this line is placed

         // Check if the error relates to width or length
        if (errorMessage.includes('width') || errorMessage.includes('length')) {
            const widthField = document.getElementById('glassWidth');
            const lengthField = document.getElementById('glassLength');

            // Highlight the fields with an error
            if (widthField) widthField.classList.add('input-error');
            if (lengthField) lengthField.classList.add('input-error');
        }
    })
    .finally(() => {
        // Hide the spinner once the request is complete
        hideSpinner();
    });
}
