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
    pvbThicknesses: [] // Array for PVB thicknesses
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

    inputParams.layersTypes = [];
    inputParams.layersThicknesses = [];
    inputParams.glassLayersStrengthType = [];
    inputParams.numberOfPlies = [];
    inputParams.pvbThicknesses = [];  // Clear the pvbThicknesses array
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
        pvbThicknesses: [] // Add the PVB thicknesses array
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
            const list4 = [5, 6, 8, 10, 12, 16, 19];

            for(let j = 0; j < numberOfPlies; j++) {
                const plyThickness = parseFloat(document.getElementById(`plyThickness${i}-${j}`).value) || 0;
                pliesTotalThickness += plyThickness;
                plyThicknessList.push(plyThickness);
            }

            let totalPvbThicknesses = 0
            for(let k = 0; k < numberOfPlies - 1; k++) {
                const pvbThickness = parseFloat(document.getElementById(`pvbThickness${i}-${k}`).value) || 0;
                inputParams.pvbThicknesses.push(pvbThickness); // Add the PVB thickness to the array
                totalPvbThicknesses += pvbThickness
            }

            // Sum pliesTotalThickness and totalPvbThicknesses
            const combinedThickness = pliesTotalThickness + totalPvbThicknesses;

            // Function to find the closest value in list4
            const findClosest = (value, list) => {
                return list.reduce((a, b) => (Math.abs(b - value) < Math.abs(a - value) ? b : a));
            };

            // Find the closest value in list4
            const closestMatch = findClosest(combinedThickness, list4);

            console.log("closestMatch", closestMatch)

            const laminatedLayerType = document.getElementById(`laminatedType${i}`).value;
            inputParams.glassLayersStrengthType.push(laminatedLayerType);
            inputParams.layersThicknesses.push(pliesTotalThickness);
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
