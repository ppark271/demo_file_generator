from utils import *

"""
Generates a capital call PDF document with the given filename and content.

Parameters:
- filename: Name of the output PDF file.
- investing_entity_name: Name of the investing entity (fund).
- legal_name: Legal name of the investor.
- image_path: Path to the logo image file.
"""
def create_capital_call_pdf(filename, investing_entity_name, legal_name, image_path, color="#515154"):
    # Create a document template with specified margins and page size
    doc = SimpleDocTemplate(
        filename, pagesize=letter,
        rightMargin=0.75 * inch, leftMargin=0.75 * inch,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch
    )

    story = []  # List to hold the flowable elements for the PDF

    # Define styles for the document
    styles = getSampleStyleSheet()

    # Update default style with built-in font
    styles['Normal'].fontName = 'Helvetica'
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 12

    # Custom styles for headings and body text
    styles.add(ParagraphStyle(
        name='CustomHeading1',
        fontName='Helvetica-Bold',
        fontSize=16,
        spaceAfter=10,
        textColor=colors.HexColor("#333333"),
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading2',
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceBefore=14,
        spaceAfter=4,
        textColor=colors.HexColor("#333333"),
    ))
    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#515154"),
        spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name='CustomEmphasis',
        parent=styles['CustomBody'],
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#000000"),
    ))
    # Style for table cells
    table_cell_style = ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#515154"),
    )
    table_cell_bold_style = ParagraphStyle(
        name='TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
    )
    placement_style = ParagraphStyle(
        name="sample_style",
        parent=table_cell_style,
        textColor = colors.HexColor(color)
    )

    # Add Logo to the document with aspect ratio maintained
    logo = create_logo(80, 40, image_path)  # Adjust max dimensions as needed
    story.append(logo)
    story.append(Spacer(1, 10))  # Add space after the logo

    # Add Title
    story.append(Paragraph("CONFIDENTIAL", styles['CustomHeading1']))

    # Prepare data for the financial table with emphasis on key numbers
    data = [
        [
            Paragraph("To:", table_cell_bold_style),
            Paragraph("Brown University", table_cell_bold_style)
        ],
        [
            Paragraph("From:", table_cell_style),
            Paragraph("Planeteer Capital")
        ],
        [
            Paragraph("RE:"),
            Paragraph("Capital Notice #7")
        ],
        [
            Paragraph("Date:"),
            Paragraph("October 1, 2024")
        ],
        [
            Paragraph("Due Date:"),
            Paragraph("October 16, 2024")
        ]
    ]

    # Create and style the financial table
    table = Table(data, colWidths=[3.5 * inch, 2 * inch], hAlign='LEFT', repeatRows=1)

    # Table style with alternate row shading and thin lines
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#333333")),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align all cells to the left
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for all cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
    ]))
    story.append(table)

    # Divider line before footer
    story.append(Spacer(1, 14))
    story.append(DividerLine(doc.width))
    story.append(Spacer(1, 6))

    paragraph = """
    In accordance with ...................................
    ..............
    ............
    .
    """
    story.append(Paragraph(paragraph))


    instructions_data = [
        [
            Paragraph("Wire Transfer Instructions"),
            Paragraph("")
        ],
        [
            Paragraph("Bank Name:"),
            Paragraph("Chase")
        ],
        [
            Paragraph("Bank Address:"),
            Paragraph("277")
        ],
        [
            Paragraph("ABA Number:"),
            Paragraph("02")
        ],
        [
            Paragraph("Account Number"),
            Paragraph("93")
        ],
        [
            Paragraph("SWIFT Code"),
            Paragraph("CHASE")
        ],
        [
            Paragraph("Reference"),
            Paragraph("Brown")
        ]

    ]

    # Create and style the financial table
    instructions_table = Table(instructions_data, colWidths=[3.5 * inch, 2 * inch], hAlign='LEFT', repeatRows=1)

    # Table style with alternate row shading and thin lines
    instructions_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#333333")),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align all cells to the left
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size for all cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafafa")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
    ]))
    story.append(instructions_table)

    story.append(Paragraph("Should you have any general questions"))

    story.append(Paragraph("Sincerely,"))

    story.append(Paragraph("Planaterr Capital, L.P."))

    story.append(Paragraph("Sophie Purdom"))

    # Build the PDF document
    doc.build(story)


if __name__ == "__main__":
    create_capital_call_pdf(
        r"C:\Users\ppark\OneDrive - GP Fund Solutions, LLC\Desktop\GPES-FILE-ENGINE\AutoDocs\output\cap_call_new\cap_call_new.pdf",
        "investing_entity_name",
        "legal_name",
        r"C:\Users\ppark\OneDrive - GP Fund Solutions, LLC\Desktop\gpes-file-engine-crms\aea-logo.png",
        "#515154"
    )