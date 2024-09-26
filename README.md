Glass Wind Load Calculator
This web application calculates the wind load on glass structures according to various parameters such as glass dimensions, supported sides, glazing type, and duration loads. It follows industry-standard practices for glass wind load calculations, particularly useful in architectural and structural applications.

Features:
Wind Load Calculations: Supports calculations for short duration (3 seconds) and long duration (30 days) loads.
Custom Glass Input: Users can input custom dimensions of glass (length, width), supported sides, and glazing types (single or double glazed).
Layered Glass: Supports multi-layer glass inputs, allowing for detailed calculation based on the number of layers, types of glass, and thicknesses.
Coefficient of Friction (COF): Automatically computes short and long duration COF values based on user inputs.
Glass Weight Calculation: Calculates glass weight based on dimensions and PVB layers.
Load Share Factor (LSF): Calculates load sharing factors for double glazing.
Graphical Output: Generates a graphical representation of the interpolated NFL values (Nominal Failure Load) for better visualization.
PDF Report: After the calculations, the app generates a PDF report containing all the details, including deflection results and glass weight.
Technologies:
Frontend: HTML5, CSS, JavaScript (with Chart.js for visualization)
Backend: Flask (Python) for managing API routes and processing calculations
PDF Generation: Generates downloadable PDF reports using Python
Data Visualization: Plotting interpolated NFL values using custom plotting scripts
Usage:
Input glass specifications such as glass length, width, supported sides, and glazing type.
Define layer properties (types, thicknesses, PVB thicknesses, etc.).
Click Calculate to process the data and retrieve the Nominal Failure Load (NFL), Coefficient of Friction (COF), and Load Share Factor (LSF).
View the NFL graph and download the PDF report with detailed results.
Future Improvements:
Improved UI/UX: Enhance the interface to provide a more interactive and user-friendly experience.
Additional Glazing Types: Support more complex glazing types and custom materials.
Dynamic Load Testing: Add support for dynamic wind load testing based on varying environmental conditions.
