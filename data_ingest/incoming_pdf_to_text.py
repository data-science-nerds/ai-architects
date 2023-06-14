import os
from pdf2image import convert_from_path
import pytesseract

# from pdf_delimiters import SECTIONS
from .pdf_delimiters import SECTIONS


def only_pdfs(incoming_pdfs_path) -> list:
    pdf_files = []
    for filename in os.listdir(incoming_pdfs_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(incoming_pdfs_path, filename)
            pdf_files.append(filepath)
    return pdf_files


def read_pdfs(incoming_pdfs_path: list) -> bool:
    paths = only_pdfs(incoming_pdfs_path)

    for path in paths:
        # Convert PDF to images
        images = convert_from_path(path)

        # Initialize a string to hold the extracted text for all sections
        all_sections_text = ""

        # Read text from each image
        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img)

            # Extract text for each section
            for section in SECTIONS:
                beginning_string = section[0]
                ending_string = section[1]

                # Find the indices of the beginning and ending strings
                begin_index = text.find(beginning_string)
                end_index = text.find(ending_string)

                # If both strings are found, extract the text between them and append it to all_sections_text
                if begin_index != -1 and end_index != -1:
                    extracted_text = text[begin_index:end_index + len(ending_string)]
                    all_sections_text += extracted_text + "\n"

        # Write the text for allSECTIONSto a file
        filename = os.path.splitext(os.path.basename(path))[0]
        directory = 'data_ingest/processed_text_files/'
        
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        print(f'extracting data for {filename}')

        with open(f'{directory}{filename}.txt', 'w') as f:
            f.write(all_sections_text)

    return True


# def read_pdfs(incoming_pdfs_path) -> bool:
#     paths: list
#     # work only on pdf's
#     paths = only_pdfs(incoming_pdfs_path)

#     for path in paths:
#         # Convert PDF to images
#         images = convert_from_path(path)

#         # Create a folder for this PDF's text files
#         base_filename = os.path.basename(path)
#         pdf_name, _ = os.path.splitext(base_filename)
#         output_dir = f'data_ingest/processed_text_files/{pdf_name}'
#         os.makedirs(output_dir, exist_ok=True)
#         print(f'writing text files for {pdf_name}')

#         try:
#             # Read text from each image
#             for i, img in enumerate(images):
#                 text = pytesseract.image_to_string(img)
#                 with open(f'{output_dir}/output{i}.txt', 'w') as f:
#                     f.write(text)
#         except Exception:
#             print(f'WARNING!! error completing file for {pdf_name}')
#     print('completed writing all text files')
#     return True
