import os
import pdfplumber

def extract_text_from_pdf(input, output):
    try:
        # Open the PDF file
        with pdfplumber.open(input) as pdf:
            extracted_text = ""
            
            # Extract text from each page
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"

        # Write the extracted text to the output text file
        with open(output, "w", encoding="utf-8") as txt_file:
            txt_file.write(extracted_text)

        print(f"Text saved!! {output}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_all_pdfs(input, output):
    try:
        # Ensure the output directory exists
        os.makedirs(output, exist_ok=True)

        # Iterate through all PDF files in the input folder
        for file_name in os.listdir(input):
            if file_name.lower().endswith(".pdf"):
                input_pdf_path = os.path.join(input, file_name)
                output_txt_path = os.path.join(output, f"{os.path.splitext(file_name)[0]}.txt")

                # Extract text from the PDF and save it to a text file
                extract_text_from_pdf(input_pdf_path, output_txt_path)
    except Exception as e:
        print(f"error: {e}")

# Folders
input_folder = r"C:\\Users\\chipr\\OneDrive\\Desktop\\final\\knit-nlp\\READ_ONLY_pattern_references"
output_folder = r"C:\\Users\\chipr\\OneDrive\\Desktop\\final\\knit-nlp\\input_patterns"

# Process all PDFs in the input folder
process_all_pdfs(input_folder, output_folder)
