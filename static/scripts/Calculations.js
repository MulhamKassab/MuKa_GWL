const inputParams = {
    specifiedDesignLoad: 0,
    glassLength: 0,
    glassWidth: 0,
    windSpeed: 0,
    glassTypeFactors: [],
    glassLayersThicknesses: []
};

const outputResults = {
    loadResistance: 0,
    centerOfGlassDeflection: 0,
    nonFactoredLoad: 0,
    loadShareFactors: []
};

// Function to update input parameters
function setInputParameters(params) {
    Object.assign(inputParams, params);
}

function calculateNonFactoredLoad(inputData) {
  fetch('http://localhost:8000/calculate_nfl', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(inputData)
    })
    .then(response => {
    if (!response.ok) {
        throw new Error('Failed to fetch NFL: ' + response.statusText);
    }
    return response.json();
    })
    .then(data => {
        console.log('NFL:', data.nfl);
        outputResults.nonFactoredLoad = parseFloat(data.nfl);
        displayResults();
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('resultDisplay').innerText = 'Error: ' + error.message;
    });
}

// Example fetchGTF function
function fetchGTF(layerType, monoType) {
    // Placeholder: actual implementation needed based on your backend API
    return fetch(`/api/get_gtf?layerType=${layerType}&monoType=${monoType}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => data.gtf)
    .catch(error => {
        console.error('Failed to fetch GTF:', error);
        return 0; // Default or error handling
    });
}


// Function to fetch LSF data based on glass thickness and the LSF table
async function fetchLSF(thickness1, thickness2, tableName) {
    fetch('http://localhost:8000/get_lsf', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ thickness1, thickness2, tableName })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch LSF data');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error('LSF data not found');
        }
        return data; // This should include LS1 and LS2 values
    })
    .catch(error => {
        console.error('Error fetching LSF:', error);
        throw error; // Rethrow the error to be caught by the calling function
    });
}


/// Calculate Load Resistance (LR)
function calculateLoadResistance() {
    const { glassTypeFactors } = inputParams;
    const { loadShareFactors, nonFactoredLoad } = outputResults;
    
    if (glassTypeFactors.length !== loadShareFactors.length) {
        throw new Error(`Mismatch in the number of layers for type factors (${glassTypeFactors.length}) and load share factors (${loadShareFactors.length})`);
    }
    const adjustmentFactor = inputParams.numberOfSupportedSides;
    outputResults.loadResistance = nonFactoredLoad * glassTypeFactors.reduce((acc, gtf, index) => acc + (gtf * loadShareFactors[index]), 0) * adjustmentFactor;
}

// Calculate Center-of-Glass Deflection
function calculateCenterOfGlassDeflection() {
   
}

// Function to display results
function displayResults() {
    document.getElementById('results').innerHTML = 
        'Load Resistance: ' + outputResults.loadResistance.toFixed(2) + 
        '<br>Non Factor Load: ' + outputResults.nonFactoredLoad.toFixed(2) + 
        '<br>Center-of-Glass Deflection: ' + outputResults.centerOfGlassDeflection.toFixed(2) +
        '<br>Load Share Factors: ' + outputResults.loadShareFactors.map(factor => factor.toFixed(4)).join(', ');
}

// Main function to run the calculations
async function main() {
  try {
      await calculateNonFactoredLoad(inputParams);
      fetchLSF();
      calculateLoadResistance();
      calculateCenterOfGlassDeflection();
      displayResults();
  } catch (error) {
      console.error("An error occurred in the calculation: ", error.message);
  }
}

// Function to be called when the "Calculate" button is clicked
async function performCalculation() {
    const specifiedDesignLoad = parseFloat(document.getElementById('specifiedDesignLoad').value);
    const glassLength = parseFloat(document.getElementById('glassLength').value);
    const glassWidth = parseFloat(document.getElementById('glassWidth').value);
    const numberOfLayers = parseInt(document.getElementById('numberOfLayers').value);

    let promises = []; // Store promises here
    let glassLayersThicknesses = []; // Correct definition and usage scope
    let glassTypeFactors = []; // Array for glass type factors

    // Loop through each layer to fetch Glass Type Factor (GTF)
    for (let i = 0; i < numberOfLayers; i++) {
        const layerType = document.getElementById(`layerType${i}`).value;
        const monoThickness = parseFloat(document.getElementById(`monoThickness${i}`).value);
        const monoType = document.getElementById(`monoType${i}`).value;

        glassLayersThicknesses.push(monoThickness); // Storing thickness for each layer

        const gtfPromise = fetchGTF(layerType, monoType)
          .then(gtf => {
            glassTypeFactors[i] = gtf; // Store GTF for each layer
          })
          .catch(error => {
            console.error(`Failed to fetch GTF for layer ${i}:`, error);
            glassTypeFactors[i] = 0; // Default to 0 in case of error
          });

        promises.push(gtfPromise);
    }

    await Promise.all(promises); // Wait for all GTF fetch operations to complete

    setInputParameters({ // Set input parameters once all data is fetched
        specifiedDesignLoad,
        glassLength,
        glassWidth,
        glassLayersThicknesses,
        glassTypeFactors
    });

    await main(); // Proceed with main calculations
}
    // After all GTF values are fetched, set parameters and perform calculations
    setInputParameters({
        specifiedDesignLoad,
        glassLength,
        glassWidth, 
    });

    // Call main calculation function
    // main();