import win32com.client

def convert_to_pdf(doc_path, pdf_path):
    # Open Word application
    word = win32com.client.Dispatch("Word.Application")
    
    # Open the Word document
    doc = word.Documents.Open(doc_path)
    
    # Save the document as PDF
    doc.SaveAs(pdf_path, FileFormat=17)  # 17 is the code for PDF format
    
    # Close the document and the Word application
    doc.Close()
    word.Quit()

# Convert the document
convert_to_pdf(r"C:\Users\ppark\OneDrive - GP Fund Solutions, LLC\Desktop\GPES-FILE-ENGINE\AutoDocs\example_filled.docx", r"C:\Users\ppark\OneDrive - GP Fund Solutions, LLC\Desktop\GPES-FILE-ENGINE\AutoDocs\example_filled.pdf")
