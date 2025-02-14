from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Define the colors from the logo
logo_red = HexColor('#DF0029')  # The red color from the logo

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MyBold', fontName='Helvetica-Bold', fontSize=10, spaceAfter=5))
styles.add(ParagraphStyle(name='MyNormal', fontName='Helvetica', fontSize=10, spaceAfter=5))
styles.add(ParagraphStyle(name='MyRedNormal', parent=styles['MyNormal'], textColor=colors.red))
styles.add(
    ParagraphStyle(name='MainTitle', fontName='Helvetica-Bold', fontSize=18, textColor=logo_red, alignment=TA_CENTER,
                   spaceAfter=20))
styles.add(
    ParagraphStyle(name='SecondTitle', fontName='Helvetica-Bold', fontSize=14, textColor=black, alignment=TA_LEFT,
                   spaceAfter=15))
styles.add(
    ParagraphStyle(name='MySubTitle', fontName='Helvetica-Bold', fontSize=10, textColor=logo_red, alignment=TA_LEFT,
                   spaceAfter=7))
styles.add(ParagraphStyle(name='MySection', fontName='Helvetica-Bold', fontSize=10, textColor=black, spaceAfter=8))


def draw_section_title(text):
    # Create a table with red background and white bold text
    title_data = [[text]]
    title_table = Table(title_data, colWidths=[480])  # Adjust width as needed
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#FF0000")),  # Red background
        ('TEXTCOLOR', (0, 0), (-1, -1), white),  # White text
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Bold font
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Font size
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left-align text
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle vertical alignment
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    return title_table


def draw_paragraph(text, style):
    return Paragraph(text, style)


def add_logo_and_text(canvas, doc, logo_path):
    # Add logo at the top-right corner
    logo = Image(logo_path, width=70, height=70)
    logo.drawOn(canvas, doc.pagesize[0] - 130, doc.pagesize[1] - 80)  # Positioning the logo

    # Set the font for the footer
    canvas.setFont('Helvetica', 10)


    # Footer text content
    footer_text = """Dubai Investment Park 2
P.O. Box 54563,
Dubai, UAE
+971 4 88 5333 6
info@gutmannpvb.com
www.gutmannpvb.com"""

    # Split footer text into lines and draw each line at the bottom of the page
    footer_lines = footer_text.split('\n')
    y_position = 20  # Adjust this to position the footer correctly from the bottom
    for line in footer_lines:
        canvas.drawString(40, y_position, line)  # Left-align text starting at x=40
        y_position += 12  # Adjust spacing between lines

# Function to draw visual glass specification table
def draw_glass_spec_table(thicknesses, plyThicknessList, pvb_thicknesses, glass_layers_strength_type, heat_treatments,
                          airGap, interlayerTypes):
    row_data = []
    layer_colors = []

    # Map heat treatments to colors
    heat_treatment_colors = {
        'annealed': HexColor("#B3E5FC"),
        'tempered': HexColor("#FFCDD2"),
        'heatStrengthened': HexColor("#e6ddc8"),
        'default': HexColor("#E0E0E0")
    }
    if glass_layers_strength_type == ["laminated", "laminated"]:
        # First Laminated Layer
        # First ply
        row_data.append(plyThicknessList[0])
        layer_colors.append(heat_treatment_colors.get(heat_treatments[0], heat_treatment_colors['default']))

        # Interlayer
        row_data.append(pvb_thicknesses[0])
        if interlayerTypes[0] == "PVB":
            layer_colors.append(HexColor("#e3fff6"))
        else:
            layer_colors.append(HexColor("#fff4e3"))

        # Second ply
        row_data.append(plyThicknessList[1])
        layer_colors.append(heat_treatment_colors.get(heat_treatments[0], heat_treatment_colors['default']))

        # Air gap
        row_data.append(airGap)
        layer_colors.append(HexColor("#f5f3f0"))

        # Second Laminated Layer
        # First ply
        row_data.append(plyThicknessList[2])
        layer_colors.append(heat_treatment_colors.get(heat_treatments[1], heat_treatment_colors['default']))

        # Interlayer
        row_data.append(pvb_thicknesses[1])
        if interlayerTypes[1] == "PVB":
            layer_colors.append(HexColor("#e3fff6"))
        else:
            layer_colors.append(HexColor("#fff4e3"))

        # Second ply
        row_data.append(plyThicknessList[3])
        layer_colors.append(heat_treatment_colors.get(heat_treatments[1], heat_treatment_colors['default']))
    else:
        ply_index = 0  # This will keep track of the position in the plyThicknessList and pvb_thicknesses
        for index, layer_type in enumerate(glass_layers_strength_type):
            if layer_type == 'laminated':
                num_plies = thicknesses[index]  # Assuming 'thicknesses[index]' holds number of plies for this index if laminated
                for _ in range(num_plies):
                    if ply_index < len(plyThicknessList):
                        # Add ply thickness
                        row_data.append(plyThicknessList[ply_index])
                        layer_colors.append(heat_treatment_colors.get(heat_treatments[index], heat_treatment_colors['default']))

                        # Check if there's a PVB layer to add after this ply
                        if ply_index < len(pvb_thicknesses):
                            row_data.append(pvb_thicknesses[ply_index])
                            if pvb_thicknesses[0] == "PVB":
                                layer_colors.append(HexColor("#e3fff6"))
                            else:
                                layer_colors.append(HexColor("#fff4e3"))

                        ply_index += 1  # Move to the next ply/PVB in the list
            else:
                # Monolithic layers
                row_data.append(thicknesses[index])
                layer_colors.append(heat_treatment_colors.get(heat_treatments[index], heat_treatment_colors['default']))

            # Check if it's time to add the air gap
            if airGap > 0 and index == 0:  # Assuming air gap should be after the first layer
                row_data.append(airGap)
                layer_colors.append(HexColor("#f5f3f0"))

    # Calculate dynamic column widths based on layer thickness
    col_widths = [max(20, min(float(cell) * 10, 100)) for cell in row_data]

    # Define row height
    row_height = 100

    # Create the table
    table_data = [row_data]
    spec_table = Table(table_data, colWidths=col_widths, rowHeights=[row_height])

    # Apply styles for custom appearance
    table_styles = [('BACKGROUND', (col_index, 0), (col_index, 0), color) for col_index, color in enumerate(layer_colors)]
    table_styles += [
        ('LINEBEFORE', (0, 0), (-1, -1), 0, colors.white),
        ('LINEAFTER', (0, 0), (-1, -1), 0, colors.white),
        ('LINEABOVE', (0, 0), (-1, -1), 0, colors.white),
        ('LINEBELOW', (0, 0), (-1, -1), 0, colors.white),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]

    # Apply the styles to the table
    spec_table.setStyle(TableStyle(table_styles))

    return spec_table



def create_pdf(fileobj, glass_length, glass_width, pvb_thicknesses, number_of_supported_sides, thicknesses,
               plyThicknessList, glass_weight, short_load, long_load, allowable_Deflection, lr, glazing_type, short_cof,
               long_cof, glass_layers_strength_type, interlayerTypes, recommended_thickness, airGap, heat_treatments,
               logo_path, first_page_image_path):
    if glass_width > glass_length:
        glass_length, glass_width = glass_width, glass_length
    doc = SimpleDocTemplate(fileobj, pagesize=A4, topMargin=30)
    elements = [
        draw_paragraph("GUTMANN PVB", styles['MainTitle']),
        draw_paragraph("Load Resistance Report", styles['SecondTitle']),
        draw_paragraph("Based on ASTM E1300", styles['MyNormal']),
        Spacer(1, 20),
    ]

    interlayer_types_str = ", ".join(interlayerTypes)
    # Glass Information and Spec Table Side by Side
    glass_info_data = [
        [draw_paragraph(f"<b>Long side (mm):</b> {glass_length}", styles['MyNormal']),
         draw_paragraph(f"<b>short side (mm):</b> {glass_width}", styles['MyNormal']),
         draw_paragraph(f"<b>Supported sides:</b> {number_of_supported_sides}", styles['MyNormal']),
         draw_paragraph(f"<b>Allowable deflection (mm):</b> {allowable_Deflection}", styles['MyNormal']),
         draw_paragraph(f"<b>Glass weight (KG):</b> {glass_weight}", styles['MyNormal']),
         draw_paragraph(f"<b>Glazing type :</b> {glazing_type}", styles['MyNormal'])
        ]
    ]
    glass_spec_table = draw_glass_spec_table(thicknesses, plyThicknessList, pvb_thicknesses, glass_layers_strength_type,
                                             heat_treatments, airGap, interlayerTypes)
    glass_info_table = Table([glass_info_data + [glass_spec_table]], colWidths=[150, 150, 150, 150, 150], hAlign="LEFT")
    glass_info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')
    ]))

    elements.append(glass_info_table)
    elements.append(Spacer(1, 20))
    # Layers Information Content
    for i, (thickness, construction_type, heat_treatment, interlayer_type) in enumerate(
            zip(thicknesses, glass_layers_strength_type, heat_treatments, interlayerTypes)):
        # Generate text for the paragraph
        layer_info_text = (
            f"<b>Layer {i + 1}:</b><br/>"
            f"<b>Thickness:</b> {thickness} mm, "
            f"<b>Lite Type:</b> {construction_type}, "
            f"<b>Heat Treatment:</b> {heat_treatment}"
        )

        # Add interlayer type if it exists for this layer
        if interlayer_type:
            layer_info_text += f", <b>Interlayer Type:</b> {interlayer_type}"

        # Append the formatted text to the document elements
        elements.append(draw_paragraph(layer_info_text, styles['MyNormal']))
        elements.append(Spacer(1, 12))  # Add spacer after each layer's info for better formatting

    elements.append(draw_paragraph("Applied Loads:", styles['MySubTitle']))
    elements.append(draw_paragraph(f"<b>Short Duration Load:</b> {short_load} kPa (3 sec)", styles['MyNormal']))
    if long_load > 0:  # Only display long duration if it's greater than 0
        elements.append(draw_paragraph(f"<b>Long Duration Load:</b> {long_load} kPa (30 days)", styles['MyNormal']))
    elements.append(Spacer(1, 12))

    elements.append(Spacer(1, 12))

    # Final result report as a table
    elements.append(draw_section_title("Final Results:"))
    elements.append(Spacer(1, 30))

    # Define standard widths for the table columns
    column_widths = [40, 80, 90, 140, 60]

    # First Table: LR and Applied Load (skip long load results if long_load is 0)
    table_data_lr = [
        ["Layer", "Duration", "LR (kPa)", "Applied Load (kPa)", "Result"]
    ]

    # Second Table: Deflection and Allowable Deflection (skip long load results if long_load is 0)
    table_data_deflection = [
        ["Layer", "Duration", "Deflection (mm)", "Allowable Deflection (mm)", "Result"]
    ]

    # Determine the number of layers to include in the report based on the glazing type
    num_layers = 1 if glazing_type == "double" else len(thicknesses)

    for i in range(num_layers):
        short_lr = lr[0]['short'][i] if 'short' in lr[0] and len(lr[0]['short']) > i else 0.0
        short_cof_result = "Accepted" if short_cof[i] < allowable_Deflection else "Not Accepted"
        short_result_lr = "Accepted" if short_lr > short_load else "Not Accepted"

        # Add rows for Short Duration in LR and Applied Load table
        table_data_lr.append([f"{i + 1}", "Short", f"{short_lr:.2f}", f"{short_load:.2f}", short_result_lr])

        # Add rows for Short Duration in Deflection table
        table_data_deflection.append(
            [f"{i + 1}", "Short", f"{short_cof[i]:.2f}", f"{allowable_Deflection:.2f}", short_cof_result])

        # If `long_load` is greater than 0, calculate and add long duration results
        if long_load > 0:
            long_lr = lr[0]['long'][i] if 'long' in lr[0] and len(lr[0]['long']) > i else 0.0
            long_cof_result = "Accepted" if long_cof[i] < allowable_Deflection else "Not Accepted"
            long_result_lr = "Accepted" if long_lr > long_load else "Not Accepted"

            # Add rows for Long Duration in LR and Applied Load table
            table_data_lr.append(["", "Long", f"{long_lr:.2f}", f"{long_load:.2f}", long_result_lr])

            # Add rows for Long Duration in Deflection table
            table_data_deflection.append(
                ["", "Long", f"{long_cof[i]:.2f}", f"{allowable_Deflection:.2f}", long_cof_result])

    # Create the first table: LR and Applied Load
    result_table_lr = Table(table_data_lr, colWidths=column_widths, hAlign="LEFT")

    # Style the first table
    result_table_lr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DF0029')),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center horizontally
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertically
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header font
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular body font
        ('TOPPADDING', (0, 1), (-1, -1), 6),  # Add padding to cells
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (1, 1), (-1, -1), colors.whitesmoke),  # Body background
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
    ]))

    # Create the second table: Deflection and Allowable Deflection
    result_table_deflection = Table(table_data_deflection, colWidths=column_widths, hAlign="LEFT")

    # Style the second table
    result_table_deflection.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DF0029')),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center horizontally
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertically
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold header font
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Regular body font
        ('TOPPADDING', (0, 1), (-1, -1), 6),  # Add padding to cells
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (1, 1), (-1, -1), colors.whitesmoke),  # Body background
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
    ]))

    # Add the first table to elements (LR and Applied Load)
    elements.append(result_table_lr)
    elements.append(Spacer(1, 20))

    # Add the second table to elements (Deflection and Allowable Deflection)
    elements.append(result_table_deflection)
    elements.append(Spacer(1, 20))

    # Add Recommended thickness after the Deflection table if necessary
    message_added = False  # Initialize a flag to control message addition

    # Check only the first layer
    first_layer_short_accepted = short_cof[0] <= allowable_Deflection
    first_layer_long_accepted = True if long_load == 0 else long_cof[0] <= allowable_Deflection

    if not first_layer_short_accepted or not first_layer_long_accepted:
        if recommended_thickness is not None:
            if not first_layer_short_accepted and recommended_thickness.get("Short"):
                elements.append(Paragraph(
                    f"NOTE: Recommended thickness for Short Duration Load to make accepted is: "
                    f"{recommended_thickness['Short']}",
                    styles['MyRedNormal']))
                elements.append(Spacer(1, 12))
            if long_load > 0 and not first_layer_long_accepted and recommended_thickness.get("Long"):
                elements.append(Paragraph(
                    f"NOTE: Recommended thickness for Long Duration Load to make accepted is: "
                    f"{recommended_thickness['Long']}",
                    styles['MyRedNormal']))
                elements.append(Spacer(1, 12))
        if not message_added:  # Check if the message has not already been added
            elements.append(Paragraph(
                "NOTE: With the current glass dimensions the deflection is not accepted, please change glass "
                "dimensions.",
                styles['MyRedNormal']))
            elements.append(Spacer(1, 12))
            message_added = True  # Set the flag to True after adding the message

    # Add the first page image directly on the canvas
    def draw_first_page(canvas, doc):
        canvas.drawImage(first_page_image_path, 0, 0, width=A4[0], height=A4[1])

    # Ensure content starts on a new page
    elements.insert(0, PageBreak())

    doc.build(elements, onFirstPage=draw_first_page,  # Full-page image on the first page
              onLaterPages=lambda canvas, doc1: add_logo_and_text(canvas, doc1, logo_path))
