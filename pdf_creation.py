from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# Define the colors from the logo
logo_red = HexColor('#DF0029')  # The red color from the logo

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MyBold', fontName='Helvetica-Bold', fontSize=10, spaceAfter=5))
styles.add(ParagraphStyle(name='MyNormal', fontName='Helvetica', fontSize=10, spaceAfter=5))
styles.add(ParagraphStyle(name='MainTitle', fontName='Helvetica-Bold', fontSize=18, textColor=logo_red, alignment=TA_LEFT,
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
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Center align text
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle vertical alignment
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),  # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    return title_table


def draw_paragraph(text, style):
    return Paragraph(text, style)


def add_logo_and_text(canvas, doc, logo_path):
    logo = Image(logo_path, width=50, height=50)
    logo.drawOn(canvas, doc.pagesize[0] - 60, doc.pagesize[1] - 60)  # Positioning the logo
    canvas.setFont('Helvetica-Bold', 12)


def create_pdf(fileobj, glass_length, glass_width, number_of_supported_sides, thicknesses, glass_weight, short_load,
               long_load, allowable_Deflection, lr, short_cof,
               long_cof, construction_types, heat_treatments, logo_path):
    doc = SimpleDocTemplate(fileobj, pagesize=A4, topMargin=30)
    elements = [
                draw_paragraph("GUTMANN PVB", styles['MainTitle']),
                draw_paragraph("Load Resistance Report", styles['SecondTitle']),
                draw_paragraph("Based on ASTM E1300", styles['MyNormal']),
                Spacer(1, 20),
                # Glass Information Section Title
                draw_section_title("Glass Information"), Spacer(1, 12),
                draw_paragraph(f"<b>Long side (mm):</b> {glass_length}", styles['MyNormal']),
                draw_paragraph(f"<b>Short side (mm):</b> {glass_width}", styles['MyNormal']),
                draw_paragraph(f"<b>Supported sides:</b> {number_of_supported_sides}", styles['MyNormal']),
                # Glass Information Content
                draw_paragraph(f"<b>Allowable deflection (mm):</b> {allowable_Deflection}", styles['MyNormal']),
                draw_paragraph(f"<b>Glass weight (KG):</b> {glass_weight}", styles['MyNormal']), Spacer(1, 12),
                # Layers Information Section Title
                draw_section_title("Layers Information"), Spacer(1, 12)]

    # Layers Information Content
    for i, (thickness, construction_type, heat_treatment) in enumerate(
            zip(thicknesses, construction_types, heat_treatments)):
        elements.append(draw_paragraph(f"Layer {i + 1}:", styles['MySubTitle']))
        elements.append(draw_paragraph(
            f"<b>Thickness</b> = {thickness} mm, <b>Lite Type</b> = {construction_type}, <b>Heat Treatment</b> = {heat_treatment}",
            styles['MyNormal']))

    elements.append(Spacer(1, 12))

    elements.append(draw_paragraph("Applied Loads:", styles['MySubTitle']))
    elements.append(draw_paragraph(f"<b>Short Duration Load:</b> {short_load} kPa (3 sec)", styles['MyNormal']))
    elements.append(draw_paragraph(f"<b>Long Duration Load:</b> {long_load} kPa (30 days)", styles['MyNormal']))
    elements.append(Spacer(1, 12))

    elements.append(Spacer(1, 12))

    # Final result report as a table
    elements.append(draw_section_title("Final Results:"))
    elements.append(Spacer(1, 12))

    # First Table: LR and Applied Load
    table_data_lr = [
        ["Layer", "Duration", "LR (kPa)", "Applied Load (kPa)", "Result"]
    ]

    # Second Table: Deflection and Allowable Deflection
    table_data_deflection = [
        ["Layer", "Duration", "Deflection (mm)", "Allowable Deflection (mm)", "Result"]
    ]

    for i in range(len(thicknesses)):
        short_lr = lr[0]['short'][i] if 'short' in lr[0] and len(lr[0]['short']) > i else 0.0
        long_lr = lr[0]['long'][i] if 'long' in lr[0] and len(lr[0]['long']) > i else 0.0

        short_cof_result = "Accepted" if short_cof[i] < allowable_Deflection else "Not Accepted"
        long_cof_result = "Accepted" if long_cof[i] < allowable_Deflection else "Not Accepted"

        # Results for LR and Applied Load
        short_result_lr = "Accepted" if short_lr > short_load else "Not Accepted"
        long_result_lr = "Accepted" if long_lr > long_load else "Not Accepted"

        # Add rows for LR and Applied Load, with merged "Layer" cell
        table_data_lr.append([f"{i + 1}", "Short", f"{short_lr:.2f}", f"{short_load:.2f}", short_result_lr])
        table_data_lr.append(["", "Long", f"{long_lr:.2f}", f"{long_load:.2f}", long_result_lr])

        # Add rows for Deflection and Allowable Deflection, with merged "Layer" cell
        table_data_deflection.append(
            [f"{i + 1}", "Short", f"{short_cof[i]:.2f}", f"{allowable_Deflection:.2f}", short_cof_result])
        table_data_deflection.append(["", "Long", f"{long_cof[i]:.2f}", f"{allowable_Deflection:.2f}", long_cof_result])

    # Create the first table: LR and Applied Load
    result_table_lr = Table(table_data_lr, hAlign="LEFT")

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
        ('SPAN', (0, 1), (0, 2)),  # Merging Layer cells for Short and Long
        ('SPAN', (0, 3), (0, 4)),  # Merging Layer cells for Short and Long for second layer
    ]))

    # Create the second table: Deflection and Allowable Deflection
    result_table_deflection = Table(table_data_deflection,  hAlign="LEFT")

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
        ('SPAN', (0, 1), (0, 2)),  # Merging Layer cells for Short and Long
        ('SPAN', (0, 3), (0, 4)),  # Merging Layer cells for Short and Long for second layer
    ]))

    # Add the first table to elements (LR and Applied Load)
    elements.append(result_table_lr)
    elements.append(Spacer(1, 12))

    # Add the second table to elements (Deflection and Allowable Deflection)
    elements.append(result_table_deflection)
    elements.append(Spacer(1, 12))

    elements.append(draw_paragraph("Notes:", styles['MyBold']))
    elements.append(
        draw_paragraph("Load resistance values are computed in accordance with ASTM E1300", styles['MyNormal']))

    doc.build(elements, onFirstPage=lambda canvas, doc1: add_logo_and_text(canvas, doc1, logo_path),
              onLaterPages=lambda canvas, doc1: add_logo_and_text(canvas, doc1, logo_path))
