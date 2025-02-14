from documents.capital_call import *
from documents.quarterly_update import *
from documents.gp_report import *
from documents.wire_instruction import *
from documents.distribution_notice import *
from documents.k1_document import *

from documents.utils import *

import tkinter as tk
from tkinter import filedialog

import os
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white
from reportlab.lib.units import inch
from io import BytesIO

from pdf_viewer import *

class MainApp(tk.Tk):
    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.label_file.config(text=f"Selected: {file_path}")
            self.selected_file.set(file_path)

            df = pd.read_excel(file_path, sheet_name = "Investor")
            investor_col = df["Legal Name"]
            for i in investor_col:
                self.investors.add(i)
            self.checked_investors = list(self.investors)

    def select_logo(self):
        logo_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")],  # Filter image file types
        )
        if logo_path:
            self.label_logo.config(text=f"Selected: {logo_path}")
            self.selected_logo.set(logo_path)

    def select_directory(self):
        output_directory = filedialog.askdirectory(title="Select Output Directory")
        if output_directory:
            self.label_dir.config(text=f"Selected: {output_directory}")
            self.selected_directory.set(output_directory)

    def option_selected(self, choice):
        self.label_option.config(text=f"Selected option: {choice}")

    def submit_action(self):
        print(self.checked_investors)
        
        excel_file_path = self.selected_file.get()
        logo_path = self.selected_logo.get()
        output_directory = self.selected_directory.get()
        option = self.selected_option.get()

        if self.is_sample:
            output_directory = "./sample/"
        if self.is_sample:
            output_pdf_name = "sample.pdf"

        if excel_file_path == "No file selected":
            print("No file selected")
            return
        if logo_path == "No logo selected":
            print("No logo selected")
            return
        if output_directory == "No directory selected":
            print("No directory selected")
            return
        if option == "No option selected":
            print("No option selectes")
            return

        color = "#515154"
        if self.is_sample:
            color = "#ff4e28"

        # Read data from the selected Excel file
        df = pd.read_excel(excel_file_path, sheet_name = "Investor")


        # Get current quarter and year for filename
        now = datetime.now()
        quarter = (now.month - 1) // 3 + 1
        quarter_str = f"Q{quarter} {now.year - 1}"

        funds = {}
        fund_names = set()

        # Iterate over each row in the DataFrame to gather all the funds
        for index, row in df.iterrows():
            fund_names.add(str(row["Fund Name"]))
        
        fund_names = list(fund_names)


        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            investing_entity_name = str(row["Fund Name"]) 
            investor_code = str(row["Investor Code"])  
            legal_name = str(row["Legal Name"]) 
            address_1 = str(row["Address 1"])
            address_2 = str(row["Address 2"])
            city = str(row["City"])
            state = str(row["State"])
            zip_code = str(row["Zip"])
            country = str(row["Country"])
            tax_id = str(row["Tax ID"])
            fund_name = str(row["Fund Name"])

            # Check if investor was checked
            if legal_name not in self.checked_investors:
                continue

            # Check if the logo path is relative or absolute
            if not os.path.isabs(logo_path):
                # If relative, construct the full path relative to the Excel file's directory
                logo_path = os.path.join(os.path.dirname(excel_file_path), logo_path)

            # Verify that the logo file exists
            if not os.path.isfile(logo_path):
                print(f"Logo file '{logo_path}' not found. Skipping {legal_name}.")
                continue

            # Sanitize investor code and legal name for filenames
            investor_code_safe = sanitize_filename(investor_code)
            fund_code_safe = sanitize_filename(investor_code[4:])
            legal_name_safe = sanitize_filename(legal_name)
            output_pdf_path = ""

            text_to_add = {
                "logo" : logo_path,
                "legal_name" : legal_name,
                "footer" : f"{fund_name}, {address_1}, {city}, {state} {zip_code}",
                "date" : datetime.now().strftime("%B %d, %Y"),
                "fund_name" : fund_name,
                "address_1" : address_1
            }

            
            # Try-except block to catch exceptions
            try:
                #capital call
                if option == "Capital Call":
                    if not self.is_sample:
                        output_pdf_name = f"{investor_code_safe}_{legal_name_safe} - {fund_name} - Capital Call.pdf"
                    output_pdf_path = os.path.join(output_directory, output_pdf_name)

                    create_capital_call_pdf(
                        output_pdf_path,
                        investing_entity_name,
                        legal_name,
                        logo_path,
                        color
                    )

                    self.files_list.append(output_pdf_path)

                
                #k1 document
                elif option == "K1 Document":
                    if not self.is_sample:
                        output_pdf_name = f"{investor_code_safe}_{legal_name_safe} - {fund_name} - K1.pdf"
            
                    output_pdf_path = os.path.join(output_directory, output_pdf_name)

                    create_k1_document_pdf(fund_name, legal_name, output_pdf_path)

                    self.files_list.append(output_pdf_path)

                #quarterly update
                elif option == "Quarterly Update":
                    #if fund has already been encountered, skip it
                    if (fund_name in funds):
                        continue
                    funds[fund_name] = 1

                    output_pdf_name_page1 = f"{fund_code_safe} Quarterly Update Page - {quarter_str}.pdf"
                    output_pdf_path_page1 = os.path.join(output_directory, output_pdf_name_page1)

                    create_quarterly_update_pdf(
                        output_pdf_path_page1,
                        investing_entity_name,
                        legal_name,
                        logo_path
                    )

                    texts_with_positions = [
                        (fund_name, (30, 760))
                    ]

                    output_pdf_name_page2 = f"{fund_code_safe} Quarterly Update Page2 - {quarter_str}.pdf"
                    output_pdf_path_page2 = os.path.join(output_directory, output_pdf_name_page2)
                    add_multiple_texts_to_existing_pdf("documents/quarterly_update_template.pdf", output_pdf_path_page2, texts_with_positions)

                    if not self.is_sample:
                        output_pdf_name = f"{fund_code_safe}_{fund_name} - Quarterly Update.pdf"
                    output_pdf_path = os.path.join(output_directory, output_pdf_name)

                    # Step 1: Open the two PDFs
                    with open(output_pdf_path_page1, "rb") as file1, open(output_pdf_path_page2, "rb") as file2:
                        reader1 = PyPDF2.PdfReader(file1)
                        reader2 = PyPDF2.PdfReader(file2)

                        # Step 2: Create a PdfWriter object to hold the combined PDFs
                        writer = PyPDF2.PdfWriter()

                        # Step 3: Add pages from the first PDF
                        for page_num in range(len(reader1.pages)):
                            page = reader1.pages[page_num]
                            writer.add_page(page)

                        # Step 4: Add pages from the second PDF
                        for page_num in range(len(reader2.pages)):
                            page = reader2.pages[page_num]
                            writer.add_page(page)

                        # Step 5: Write the combined PDF to a new file
                        with open(output_pdf_path, "wb") as output_file:
                            writer.write(output_file)

                    # Step 6: Delete the original PDFs
                    os.remove(output_pdf_path_page1)
                    os.remove(output_pdf_path_page2)

                    self.files_list.append(output_pdf_path)
                    
                #gp report
                elif option == "GP Report":
                    #if fund has already been encountered, skip it
                    if (fund_name in funds):
                        continue
                    funds[fund_name] = 1

                    if not self.is_sample:
                        output_pdf_name = f"{fund_code_safe}_{fund_name} - GP Report.pdf"

                    output_pdf_path = os.path.join(output_directory, output_pdf_name)

                    footer = f"{investing_entity_name}, {address_1}, {city}, {state}, {zip_code}"
                    create_gp_report_pdf(
                        output_pdf_path,
                        investing_entity_name,
                        legal_name,
                        logo_path,
                        fund_names,
                        footer)

                    self.files_list.append(output_pdf_path)

                #wire instruction confirmation
                elif option == "Wire Instruction":
                    if not self.is_sample:
                        output_pdf_name = f"{investor_code_safe}_{legal_name_safe} - {fund_name} - Wire Instructions.pdf"

                    output_pdf_path = os.path.join(output_directory, output_pdf_name)

                    create_wire_instruction_pdf(text_to_add, output_pdf_path)

                    self.files_list.append(output_pdf_path)

                #distribution notice
                elif option == "Distribution Notice":
                    if not self.is_sample:
                        output_pdf_name = f"{investor_code_safe}_{legal_name_safe} - {fund_name} - Distribution Notice.pdf"

                    output_pdf_path = os.path.join(output_directory, output_pdf_name)

                    text_to_add = {
                            "logo" : logo_path,
                            "legal_name" : legal_name_safe,
                            "date" : datetime.now().strftime("%B %d, %Y"),
                            "fund_name" : fund_name,
                            "address_1" : address_1,
                            "state" : state,
                            "city" : city,
                            "zip_code" : zip_code,
                        }

                    create_distribution_notice_pdf(text_to_add, output_pdf_path)

                    self.files_list.append(output_pdf_path)

                
                print(f"Generating PDF for {legal_name} at {output_pdf_path}")
                    
            except PermissionError as e:
                print(f"Failed to write PDF for {legal_name}: {e}")
            except Exception as e:
                print(f"An error occurred while generating PDF for {legal_name}: {e}")

            if self.is_sample:
                self.files_list = []
                break
            

        if (self.bulk_choice.get()):
            self.run_merge()
        self.files_list = []
        
        
        print("PDF generation complete.")
    
    def run_merge(self):
        start_delim = self.start_delimiter.get()
        end_delim = self.end_delimiter.get()
        output_filename = self.output_file.get()
        output_dir = self.selected_directory.get()
        if not self.files_list or not start_delim or not end_delim or not output_filename or not output_dir:
            print("Please fill all fields")
            return
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
        output_path = os.path.join(output_dir, output_filename)
        self.merge_pdfs(self.files_list, start_delim, end_delim, output_path)

    def merge_pdfs(self, files, start_delim, end_delim, output_path):
        pdf_writer = PdfWriter()
        # files is a tuple of file paths
        files = list(files)
        files.sort()  # Optional: sort files alphabetically
        for filepath in files:
            filename = os.path.basename(filepath)
            investor_code = filename.split('_')[0]
            full_code = f"{start_delim}{investor_code}{end_delim}"
            pdf_reader = PdfReader(filepath)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                width = float(page.mediabox.width)
                height = float(page.mediabox.height)
                packet = BytesIO()
                # Create a new PDF with ReportLab
                can = canvas.Canvas(packet, pagesize=(width, height))
                can.setFillColor(white)
                # Place the text at top-right corner
                margin = inch * 0.5  # Half an inch margin
                text_width = can.stringWidth(full_code)
                x = width - text_width - margin
                y = height - margin
                can.drawString(x, y, full_code)
                can.save()
                # Move to the beginning of the StringIO buffer
                packet.seek(0)
                overlay_pdf = PdfReader(packet)
                overlay_page = overlay_pdf.pages[0]
                page.merge_page(overlay_page)
                pdf_writer.add_page(page)

            if (self.split_choice.get()):
                continue
            os.remove(filepath)

        with open(output_path, 'wb') as out_file:
            pdf_writer.write(out_file)
        print(f"Merged PDF saved as {output_path}")
    

    def __init__(self):
        super().__init__()
        self.title("AutoDocs")
        # Set the window size
        self.geometry("1280x1000")
        self.config(bg="#f0f0f0")  # Background color

        # Variables to store user selections
        self.selected_file = tk.StringVar(self, value="No file selected")
        self.selected_logo = tk.StringVar(self, value="No logo selected")
        self.selected_directory = tk.StringVar(self, value="No directory selected")

        self.label_file = ""
        self.label_logo = ""
        self.label_dir = ""

        self.investors = set()
        self.checked_investors = list(self.investors)

        self.is_sample = False

        # Create a StringVar to hold the choice (split or bulk)
        self.split_choice = tk.IntVar(value=1)
        self.bulk_choice = tk.IntVar(value=0)
        self.start_delimiter = tk.StringVar(self, value = "<start>")
        self.end_delimiter = tk.StringVar(self, value = "<end>")
        self.output_file = tk.StringVar(self, value = "bulk.pdf")

        self.files_list = []

        # Define font and styling options
        self.font_label = ("Helvetica", 12)
        self.font_button = ("Helvetica", 12, "bold")

        # Create a container to hold the frames (pages)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold pages
        self.frames = {}

        # Initialize all the pages
        for F in (InputPage, OutputPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page initially
        self.show_frame("InputPage")

    def show_frame(self, page_name):
        # Bring the frame to the front
        frame = self.frames[page_name]
        frame.tkraise()
        

class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        def on_next():
            controller.is_sample = True

            controller.show_frame("OutputPage")
            controller.submit_action()

            # open pdf file
            #file_name = r"C:\Users\ppark\OneDrive - GP Fund Solutions, LLC\Desktop\GPES-FILE-ENGINE\AutoDocs\output\wire_instructions\bulk.pdf"
            file_name = "./sample/sample.pdf"
            if not os.path.isfile(file_name):
                return
            doc = fitz.open(file_name)
            sample_output(controller.frames["OutputPage"].frame_sample, doc)
            controller.is_sample = False

        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text="GPES FileGen", font=('Arial', 16))
        label.pack(side="top", fill="x", pady=10)

        # Frame for file selection
        frame_file = tk.Frame(self, bg="#e6e6e6", bd=2, relief="sunken", padx=10, pady=10)
        frame_file.pack(padx=20, pady=20, fill="x")

        label_file_title = tk.Label(frame_file, text="Select CRM Excel File", font=controller.font_label, bg="#e6e6e6")
        label_file_title.pack(anchor="w")

        button_file = tk.Button(frame_file, text="Select File", command=controller.select_file, font=controller.font_button, bg="#4CAF50", fg="white")
        button_file.pack(side="left", padx=10, pady=5)

        controller.label_file = tk.Label(frame_file, textvariable=controller.selected_file, bg="#e6e6e6", font=controller.font_label)
        controller.label_file.pack(side="left", padx=10)

        # Frame for logo selection
        frame_logo = tk.Frame(self, bg="#e6e6e6", bd=2, relief="sunken", padx=10, pady=10)
        frame_logo.pack(padx=20, pady=20, fill="x")

        label_logo_title = tk.Label(frame_logo, text="Select Logo To Be Placed On Documents", font=controller.font_label, bg="#e6e6e6")
        label_logo_title.pack(anchor="w")

        button_logo = tk.Button(frame_logo, text="Select Logo", command=controller.select_logo, font=controller.font_button, bg="#4CAF50", fg="white")
        button_logo.pack(side="left", padx=10, pady=5)

        controller.label_logo = tk.Label(frame_logo, textvariable=controller.selected_logo, bg="#e6e6e6", font=controller.font_label)
        controller.label_logo.pack(side="left", padx=10)

        # Frame for the option menu
        frame_option = tk.Frame(self, bg="#e6e6e6", bd=2, relief="sunken", padx=10, pady=10)
        frame_option.pack(padx=20, pady=20, fill="x")

        label_option_title = tk.Label(frame_option, text="Select An Option", font=controller.font_label, bg="#e6e6e6")
        label_option_title.pack(anchor="w")

        options = ["Capital Call", "Distribution Notice", "GP Report", "Wire Instruction", "Quarterly Update", "K1 Document"]
        controller.selected_option = tk.StringVar(self)
        controller.selected_option.set(options[0])

        option_menu = tk.OptionMenu(frame_option, controller.selected_option, *options, command=controller.option_selected)
        option_menu.config(font=controller.font_button, bg="#4CAF50", fg="white")
        option_menu.pack(side="left", padx=10, pady=5)

        controller.label_option = tk.Label(frame_option, text="No option selected", bg="#e6e6e6", font=controller.font_label)
        controller.label_option.pack(side="left", padx=10)

        # Frame for the investors input
        frame_investors = tk.Frame(self, bg="#e6e6e6", bd=2, relief="sunken", padx=10, pady=10)
        frame_investors.pack(padx=20, pady=20, fill="x")

        self.select_all = True
        investors_button = tk.Button(frame_investors, text="Select Investors", command=self.show_investors)
        investors_button.pack()
        
        # Button to go to next page
        button1 = tk.Button(self, text="Next", command= on_next)
        button1.pack()

    def show_investors(self):
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_mouse_wheel(event):
            # Cross-platform scrolling using event.delta
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def update_list():
            # Keep only the items that are checked (i.e., where investor_value.get() == 1)
            self.controller.checked_investors = [item for i, item in enumerate(item_list, 1) if vars[i].get() == 1]
            print(self.controller.checked_investors)

        def select_all():
            if (vars[0].get() == 1):
                self.controller.checked_investors = self.controller.investors
                for i in checkboxes:
                    i.select()
                self.select_all = True
            else:
                self.controller.checked_investors = []
                for i in checkboxes:
                    i.deselect()
                self.select_all = False

        def create_checkboxes():
            # Create checkbox for selecting all
            select_value = tk.IntVar(value=self.select_all)
            vars.append(select_value)
            checkbox = tk.Checkbutton(scrollable_frame, text="Select All", variable=select_value, command=select_all)
            checkbox.pack(anchor="w", pady=5)
            checkboxes.append(checkbox)

            # Create checkboxes for each item in the list
            for i, item in enumerate(item_list):
                investor_value = tk.IntVar(value=(item in self.controller.checked_investors))  # Variable to track the state of the checkbox
                vars.append(investor_value)
                checkbox = tk.Checkbutton(scrollable_frame, text=item, variable=investor_value, command=update_list)
                checkbox.pack(anchor="w", pady=5)
                checkboxes.append(checkbox)

        # Use Toplevel instead of Tk to create a popup window
        window = tk.Toplevel()
        window.title("Scrollable Checkboxes")
        window.geometry("400x400")

        # Create a canvas and scrollbar
        canvas = tk.Canvas(window)
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Configure canvas to work with scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configure canvas to work with mouse
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        # Create a frame inside the canvas
        scrollable_frame = tk.Frame(canvas)

        # Create a window inside the canvas that contains the frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind the frame size changes to update the canvas scrollregion
        scrollable_frame.bind("<Configure>", on_frame_configure)

        item_list = list(self.controller.investors)

        # Lists to store checkbox variables and checkbox widgets
        vars = []
        checkboxes = []

        # Create checkboxes for each item in the list
        create_checkboxes()

        window.mainloop()
     



class OutputPage(tk.Frame):
    def __init__(self, parent, controller):
        def toggle_bulk_entry():
            # Show or hide the entry widget based on the selected option
            if controller.bulk_choice.get():
                self.bulk_frame.pack()
            else:
                self.bulk_frame.pack_forget()

        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="GPES FileGen", font=('Arial', 16))
        label.pack(side="top", fill="x", pady=10)

        frame_left = tk.Frame(self)
        frame_left.pack(side = "left", fill = "both")

        # Create a frame for directory selection
        frame_dir = tk.Frame(frame_left, bg="#e6e6e6", bd=2, relief="sunken", padx=10, pady=10)
        frame_dir.pack(padx=20, pady=20, fill="x")

        label_dir_title = tk.Label(frame_dir, text="Select Where To Store Output PDF", font=controller.font_label, bg="#e6e6e6")
        label_dir_title.pack(anchor="w")

        button_dir = tk.Button(frame_dir, text="Select Output Directory", command=controller.select_directory, font=controller.font_button, bg="#4CAF50", fg="white")
        button_dir.pack(side="left", padx=10, pady=5)

        controller.label_dir = tk.Label(frame_dir, textvariable=controller.selected_directory, bg="#e6e6e6", font=controller.font_label)
        controller.label_dir.pack(side="left", padx=10)

        # Create a frame for choosing between split and bulk
        frame_output_choice = tk.Frame(frame_left, bg="#e6e6e6", bd=2, relief="sunken", padx=10, pady=10)
        frame_output_choice.pack(padx=20, pady=20, fill="x")

        label_options = tk.Label(frame_output_choice, text="Select Output Format", font=controller.font_label, bg="#e6e6e6")
        label_options.pack(anchor="w")

        split_option = tk.Checkbutton(frame_output_choice, text="Split", variable=controller.split_choice, command=toggle_bulk_entry)
        bulk_option = tk.Checkbutton(frame_output_choice, text="Bulk", variable=controller.bulk_choice, command=toggle_bulk_entry)

        split_option.pack(anchor="w")
        bulk_option.pack(anchor="w")

        # Create an Entry widget for bulk input, but don't pack it initially
        self.bulk_frame = tk.Frame(frame_output_choice)

        tk.Label(self.bulk_frame, text="Start Delimiter:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.bulk_frame, textvariable=controller.start_delimiter).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.bulk_frame, text="End Delimiter:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.bulk_frame, textvariable=controller.end_delimiter).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.bulk_frame, text="Output File Name:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        tk.Entry(self.bulk_frame, textvariable=controller.output_file).grid(row=3, column=1, padx=5, pady=5)


        

        # Create a frame to show sample pdf
        self.frame_sample = Frame(self)
        self.frame_sample.pack(side = "left", fill = "both")

        

        frame_buttons = tk.Frame(self)
        frame_buttons.pack(side = "bottom", fill = "both")
        # Button to go back a page
        back_button = tk.Button(frame_buttons, text="Back",
                                command=lambda: controller.show_frame("InputPage"))
        back_button.pack()


        submit_button = tk.Button(frame_buttons, text="Submit", command = controller.submit_action)
        submit_button.pack()

        




if __name__ == "__main__":
    file_name = "./sample/sample.pdf"
    if os.path.isfile(file_name):
        os.remove(file_name)

    app = MainApp()
    app.mainloop()
