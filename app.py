from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename

# Import your PDF generation functions here:
# from documents.capital_call import *
# from documents.quarterly_update import *
# from documents.gp_report import *
# from documents.wire_instruction import *
# from documents.distribution_notice import *
# from documents.k1_document import *
# from documents.utils import *


app = Flask(__name__)

# Configuration for file upload
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Handle file upload
        if 'excel_file' not in request.files:
            return 'No file part'
        excel_file = request.files['excel_file']
        logo_file = request.files['logo_file']

        if excel_file and allowed_file(excel_file.filename):
            excel_filename = secure_filename(excel_file.filename)
            excel_file.save(os.path.join(app.config['UPLOAD_FOLDER'], excel_filename))

        if logo_file and allowed_file(logo_file.filename):
            logo_filename = secure_filename(logo_file.filename)
            logo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))

        option = request.form.get('option')
        output_directory = app.config['OUTPUT_FOLDER']

        # Process Excel and generate PDFs
        process_files(excel_filename, logo_filename, option, output_directory)

        return redirect(url_for('download_file', filename='generated_output.pdf'))

    return render_template('upload.html')


def process_files(excel_filename, logo_filename, option, output_directory):
    # Read data from the uploaded Excel file
    excel_file_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)
    df = pd.read_excel(excel_file_path)

    now = datetime.now()
    quarter = (now.month - 1) // 3 + 1
    quarter_str = f"Q{quarter} {now.year - 1}"

    # Example: Generate a sample PDF based on the user's selection
    output_pdf_path = os.path.join(output_directory, "generated_output.pdf")

    # Sample logic for generating different PDFs
    if option == "Capital Call":
        # Call your function to generate a Capital Call PDF
        # create_capital_call_pdf(output_pdf_path, ...)
        pass
    elif option == "K1 Document":
        # Call your function to generate a K1 Document PDF
        # create_k1_document_pdf(output_pdf_path, ...)
        pass
    # Add other cases based on the option selected


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
