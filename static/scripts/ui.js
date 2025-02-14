let thicknessOptions = []

function updateSupportedSides() {
    const supportedSides = document.getElementById('numberOfSupportedSides').value;

    // Update Length and Width Labels
    const lengthLabel = document.querySelector('label[for="glassLength"]');
    const widthLabel = document.querySelector('label[for="glassWidth"]');
    const widthInput = document.getElementById('glassWidth');


     if (supportedSides === "2" || supportedSides === "1") {
        lengthLabel.textContent = "Unsupported Length (mm)";
        widthLabel.textContent = "Supported Length (mm)";
        widthLabel.style.display = "block"; // Show width field for 2-sided support
        widthInput.style.display = "block";
        widthInput.setAttribute('required', 'required'); // Add the required attribute
    } else if (supportedSides === "4") {
        lengthLabel.textContent = "Length (mm)";
        widthLabel.textContent = "Width (mm)";
        widthLabel.style.display = "block"; // Show width field for 4-sided support
        widthInput.style.display = "block";
        widthInput.setAttribute('required', 'required'); // Add the required attribute
    }

    // Define the options for the thickness dropdown with formatted values
    const thicknessOptions_4_sided = [
        {value: 2.5, display: '2.5 (2.16)'},
        {value: 2.7, display: '2.7 (2.59)'},
        {value: 3.0, display: '3.0 (2.92)'},
        {value: 4.0, display: '4.0 (3.78)'},
        {value: 5.0, display: '5.0 (4.57)'},
        {value: 6.0, display: '6.0 (5.56)'},
        {value: 8.0, display: '8.0 (7.42)'},
        {value: 10.0, display: '10.0 (9.02)'},
        {value: 12.0, display: '12.0 (11.91)'},
        {value: 16.0, display: '16.0 (15.09)'},
        {value: 19.0, display: '19.0 (18.26)'},
        {value: 22.0, display: '22.0 (21.44)'}
    ];

    // Define the options for the thickness dropdown with formatted values
    const thicknessOptions_1_2_sided = [
        {value: "", display: 'Select layer thickness'},
        {value: 6.0, display: '6.0 (5.56)'},
        {value: 8.0, display: '8.0 (7.42)'},
        {value: 10.0, display: '10.0 (9.02)'},
        {value: 12.0, display: '12.0 (11.91)'},
        {value: 16.0, display: '16.0 (15.09)'},
        {value: 19.0, display: '19.0 (18.26)'},
        {value: 22.0, display: '22.0 (21.44)'}
    ];

    if (supportedSides == 4){
        thicknessOptions = thicknessOptions_4_sided
    }

    else{
        thicknessOptions = thicknessOptions_1_2_sided
    }
    const dropdownsToUpdate = document.querySelectorAll('.thickness-select');
    dropdownsToUpdate.forEach(dropdown => {
        // Clear existing options
        dropdown.innerHTML = '';
        // Append new options
        thicknessOptions.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.display;
            dropdown.appendChild(optionElement);
        });
    });
}

function updateGlazingType() {
    const glazingType = document.getElementById('glazingType').value;
    const layerInputsContainer = document.getElementById('layerInputs');
    let layerInputsHTML = '';

    if (glazingType === 'single') {
        layerInputsHTML = `
            <div class="form-group">
                <label for="layerType0">Single Glazed Layer Type:</label>
                <select id="layerType0" name="layerType0" onchange="updateLayerDetails(0)" required>
                    <option value="">Select Type</option>
                    <option value="mono">Monolithic</option>
                    <option value="laminated">Laminated</option>
                </select>
            </div>
            <div id="layerDetails0"></div>
        `;
    } else if (glazingType === 'double') {
        for (let i = 0; i < 2; i++) {
            layerInputsHTML += `
                <div class="form-group">
                    <label for="layerType${i}">Double Glazed Layer ${i + 1} Type:</label>
                    <select id="layerType${i}" name="layerType${i}" onchange="updateLayerDetails(${i})" required>
                        <option value="">Select Type</option>
                        <option value="mono">Monolithic</option>
                        <option value="laminated">Laminated</option>
                    </select>
                </div>
                <div id="layerDetails${i}"></div>
            `;
                // Add the Air Gap input after the first layer
            if (i === 0) {
                layerInputsHTML += `
                    <div class="form-group">
                        <label for="airGap">Air Gap (mm):</label>
                        <input type="number" id="airGap" name="airGap" required>
                    </div>
                `;
            }
        }
    }

    layerInputsContainer.innerHTML = layerInputsHTML;
    addInputEventListeners(); // Reapply listeners for dynamically generated fields
}

function updateLayerDetails(layerIndex) {
    const layerType = document.getElementById(`layerType${layerIndex}`).value;
    const layerDetailsContainer = document.getElementById(`layerDetails${layerIndex}`);
    const supportedSides = document.getElementById('numberOfSupportedSides').value;


    layerDetailsContainer.innerHTML = '';



    if (layerType === 'mono') {
        layerDetailsContainer.innerHTML = `
            <div class="form-group">
                <label for="monoThickness${layerIndex}">Layer ${layerIndex + 1} Thickness (mm):</label>
                <select id="monoThickness${layerIndex}" name="monoThickness${layerIndex}" required>
                    ${thicknessOptions.map(option => `<option value="${option.value}">${option.display}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="monoType${layerIndex}">Glass Strength of Layer ${layerIndex + 1}:</label>
                <select id="monoType${layerIndex}" name="monoType${layerIndex}" required>
                    <option value="">Select Type</option>
                    <option value="annealed">Annealed</option>
                    <option value="heatStrengthened">Heat Strengthened</option>
                    <option value="tempered">Tempered</option>
                </select>
            </div>
        `;
    } else if (layerType === 'laminated') {
        layerDetailsContainer.innerHTML = `
            <div class="form-group">
                <label for="numPlys${layerIndex}">Number of Plies for Layer ${layerIndex + 1}:</label>
                <input type="number" id="numPlys${layerIndex}" name="numPlys${layerIndex}" value ="2" onchange="updatePlys(${layerIndex})" readonly required>
            </div>
            <div id="plyDetails${layerIndex}"></div>
            <div class="form-group">
                <label for="laminatedType${layerIndex}">Glass Strength of Laminated Layer ${layerIndex + 1}:</label>
                <select id="laminatedType${layerIndex}" name="laminatedType${layerIndex}" required>
                    <option value="">Select Type</option>
                    <option value="annealed">Annealed</option>
                    <option value="heatStrengthened">Heat Strengthened</option>
                    <option value="tempered">Tempered</option>
                </select>
            </div>
        `;
        updatePlys(layerIndex);
    }
    addInputEventListeners(); // Reapply listeners for dynamically generated fields
}

function updatePlys(layerIndex) {
    numPlys = 2;
    const plyDetailsContainer = document.getElementById(`plyDetails${layerIndex}`);

    plyDetailsContainer.innerHTML = '';

    // Define the options for the ply thickness dropdown with formatted values
    const thicknessOptions = [
        {value: "", display: 'Select ply thickness'},
        {value: 2.5, display: '2.5 (2.16)'},
        {value: 2.7, display: '2.7 (2.59)'},
        {value: 3.0, display: '3.0 (2.92)'},
        {value: 4.0, display: '4.0 (3.78)'},
        {value: 5.0, display: '5.0 (4.57)'},
        {value: 6.0, display: '6.0 (5.56)'},
        {value: 8.0, display: '8.0 (7.42)'},
        {value: 10.0, display: '10.0 (9.02)'},
//        {value: 12.0, display: '12.0 (11.91)'},
//        {value: 16.0, display: '16.0 (15.09)'},
//        {value: 19.0, display: '19.0 (18.26)'},
//        {value: 22.0, display: '22.0 (21.44)'}
    ];

    // Define the options for the PVB thickness dropdown with formatted values
    const interlayerThicknessOptions = [
        {value: "", display: 'Select interlayer thickness'},
        {value: 0.381, display: '0.381 mm'},
        {value: 0.762, display: '0.762 mm'},
        {value: 1.143, display: '1.143 mm'},
        {value: 1.524, display: '1.524 mm'},
        {value: 1.905, display: '1.905 mm'},
        {value: 2.286, display: '2.286 mm'},
        {value: 2.667, display: '2.667 mm'},
        {value: 3.048, display: '3.048 mm'}
    ];

    // Define the options for the PVB/SGP interlayer dropdown
    const interlayerOptions = [
        {value: '', display: 'Select Interlayer type'},
        {value: 'PVB', display: 'PVB'},
        {value: 'SGP', display: 'SGP'}
    ];

    // Loop through each ply and create a dropdown for the thickness
    for (let i = 0; i < numPlys; i++) {
        plyDetailsContainer.innerHTML += `
            <div class="form-group">
                <label for="plyThickness${layerIndex}-${i}">Ply ${i + 1} Thickness (mm):</label>
                <select id="plyThickness${layerIndex}-${i}" name="plyThickness${layerIndex}-${i}" required>
                    ${thicknessOptions.map(option => `<option value="${option.value}">${option.display}</option>`).join('')}
                </select>
            </div>
        `;
        if (i < numPlys - 1) {
            plyDetailsContainer.innerHTML += `
                <div class="form-group">
                    <label for="interlayerType${layerIndex}-${i}">Interlayer Type:</label>
                    <select id="interlayerType${layerIndex}-${i}" name="interlayerType${layerIndex}-${i}" required>
                        ${interlayerOptions.map(option => `<option value="${option.value}">${option.display}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label for="interlayerThickness${layerIndex}-${i}">Interlayer Thickness (mm):</label>
                    <select id="interlayerThickness${layerIndex}-${i}" name="interlayerThickness${layerIndex}-${i}" required>
                        ${interlayerThicknessOptions.map(option => `<option value="${option.value}">${option.display}</option>`).join('')}
                    </select>
                </div>
            `;
        }
    }
    addInputEventListeners(); // Reapply listeners for dynamically generated fields

}

function addInputEventListeners() {
    const inputFields = document.querySelectorAll('input[required], select[required]');

    inputFields.forEach(field => {
        field.addEventListener('change', () => {
            field.classList.remove('input-error'); // Remove error class if previously applied
            field.classList.add('input-changed');  // Add "input-changed" class to show the field has been edited
        });
    });
}

// Call the function after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    addInputEventListeners();
});

