function updateGlazingType() {
    const glazingType = document.getElementById('glazingType').value;
    const layerInputsContainer = document.getElementById('layerInputs');
    let layerInputsHTML = '';

    if (glazingType === 'single') {
        layerInputsHTML = `
            <div class="form-group">
                <label for="layerType0">Single Glazed Layer Type:</label>
                <select id="layerType0" name="layerType0" onchange="updateLayerDetails(0)">
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
                    <select id="layerType${i}" name="layerType${i}" onchange="updateLayerDetails(${i})">
                        <option value="">Select Type</option>
                        <option value="mono">Monolithic</option>
                        <option value="laminated">Laminated</option>
                    </select>
                </div>
                <div id="layerDetails${i}"></div>
            `;
        }
    }

    layerInputsContainer.innerHTML = layerInputsHTML;
}

function updateLayerDetails(layerIndex) {
    const layerType = document.getElementById(`layerType${layerIndex}`).value;
    const layerDetailsContainer = document.getElementById(`layerDetails${layerIndex}`);

    layerDetailsContainer.innerHTML = '';

    // Define the options for the thickness dropdown with formatted values
    const thicknessOptions = [
        {value: null, display: 'Select layer thickness'},
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

    if (layerType === 'mono') {
        layerDetailsContainer.innerHTML = `
            <div class="form-group">
                <label for="monoThickness${layerIndex}">Layer ${layerIndex + 1} Thickness (mm):</label>
                <select id="monoThickness${layerIndex}" name="monoThickness${layerIndex}">
                    ${thicknessOptions.map(option => `<option value="${option.value}">${option.display}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label for="monoType${layerIndex}">Glass Strength of Layer ${layerIndex + 1}:</label>
                <select id="monoType${layerIndex}" name="monoType${layerIndex}">
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
                <input type="number" id="numPlys${layerIndex}" name="numPlys${layerIndex}" required min="1" onchange="updatePlys(${layerIndex})">
            </div>
            <div id="plyDetails${layerIndex}"></div>
            <div class="form-group">
                <label for="laminatedType${layerIndex}">Glass Strength of Laminated Layer ${layerIndex + 1}:</label>
                <select id="laminatedType${layerIndex}" name="laminatedType${layerIndex}">
                    <option value="">Select Type</option>
                    <option value="annealed">Annealed</option>
                    <option value="heatStrengthened">Heat Strengthened</option>
                    <option value="tempered">Tempered</option>
                </select>
            </div>
        `;
    }
}


function updatePlys(layerIndex) {
    const numPlys = parseInt(document.getElementById(`numPlys${layerIndex}`).value);
    const plyDetailsContainer = document.getElementById(`plyDetails${layerIndex}`);

    plyDetailsContainer.innerHTML = '';

    // Define the options for the ply thickness dropdown with formatted values
    const thicknessOptions = [
        {value: null, display: 'Select ply thickness'},
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

    // Define the options for the PVB thickness dropdown with formatted values
    const pvbOptions = [
        {value: null, display: 'Select PVB thickness'},
        {value: 0.381, display: '0.381 mm'},
        {value: 0.762, display: '0.762 mm'},
        {value: 1.143, display: '1.143 mm'},
        {value: 1.524, display: '1.524 mm'},
        {value: 1.905, display: '1.905 mm'},
        {value: 2.286, display: '2.286 mm'},
        {value: 2.667, display: '2.667 mm'},
        {value: 3.048, display: '3.048 mm'}
    ];

    // Loop through each ply and create a dropdown for the thickness
    for (let i = 0; i < numPlys; i++) {
        plyDetailsContainer.innerHTML += `
            <div class="form-group">
                <label for="plyThickness${layerIndex}-${i}">Ply ${i + 1} Thickness (mm):</label>
                <select id="plyThickness${layerIndex}-${i}" name="plyThickness${layerIndex}-${i}">
                    ${thicknessOptions.map(option => `<option value="${option.value}">${option.display}</option>`).join('')}
                </select>
            </div>
        `;
        if (i < numPlys - 1) {
            plyDetailsContainer.innerHTML += `
                <div class="form-group">
                    <label for="pvbThickness${layerIndex}-${i}">PVB Thickness (mm) after Ply ${i + 1}:</label>
                    <select id="pvbThickness${layerIndex}-${i}" name="pvbThickness${layerIndex}-${i}">
                        ${pvbOptions.map(option => `<option value="${option.value}">${option.display}</option>`).join('')}
                    </select>
                </div>
            `;
        }
    }
}



function createBar(flexBasis, backgroundColor, thickness) {
    const barContainer = document.createElement('div');
    barContainer.classList.add('bar-container');

    const bar = document.createElement('div');
    bar.classList.add('bar');
    bar.style.flex = `0 0 ${Math.min(flexBasis, 100)}%`;
    bar.style.backgroundColor = backgroundColor;

    const label = document.createElement('div');
    label.classList.add('bar-label');
    label.textContent = `${thickness} mm`;

    barContainer.appendChild(bar);
    barContainer.appendChild(label);

    return barContainer;
}

function gatherLayerDataAndUpdateChart() {
    const thicknessArray = [];
    const colorsArray = [];
    const glazingType = document.getElementById('glazingType').value;
    const numberOfLayers = glazingType === 'single' ? 1 : 2;

    for (let i = 0; i < numberOfLayers; i++) {
        const layerType = document.getElementById(`layerType${i}`).value;
        if (layerType === 'mono') {
            const thickness = parseFloat(document.getElementById(`monoThickness${i}`).value) || 0;
            thicknessArray.push(thickness);
            colorsArray.push(getColorByType(document.getElementById(`monoType${i}`).value));
        } else if (layerType === 'laminated') {
            const numPlys = parseInt(document.getElementById(`numPlys${i}`).value);
            for (let j = 0; j < numPlys; j++) {
                const thickness = parseFloat(document.getElementById(`plyThickness${i}-${j}`).value) || 0;
                thicknessArray.push(thickness);
                colorsArray.push(getColorByType(document.getElementById(`plyType${i}-${j}`).value));
                if (j < numPlys - 1) {
                    const pvbThickness = parseFloat(document.getElementById(`pvbThickness${i}-${j}`).value) || 0;
                    thicknessArray.push(pvbThickness);
                    colorsArray.push('grey');
                }
            }
        }
    }
    updateChart(thicknessArray, colorsArray);
}

function updateChart(thicknessArray, colorsArray) {
    const chartContainer = document.getElementById('chartContainer');
    if (!chartContainer) {
        console.error("chartContainer not found");
        return;
    }
    chartContainer.innerHTML = '';

    const totalThickness = thicknessArray.reduce((acc, val) => acc + val, 0);

    thicknessArray.forEach((thickness, index) => {
        const flexBasis = (thickness / totalThickness) * 100;
        const barBackgroundColor = colorsArray[index] || 'transparent';
        const bar = createBar(flexBasis, barBackgroundColor, thickness);
        chartContainer.appendChild(bar);
    });
}

function getColorByType(type) {
    switch (type) {
        case 'annealed':
            return 'blue';
        case 'heatStrengthened':
            return 'orange';
        case 'tempered':
            return 'red';
        default:
            return 'grey';
    }
}
