import os
from pdf2image import convert_from_path
import pytesseract


def only_pdfs(incoming_pdfs_path):
    pdf_files = []
    for filename in os.listdir(incoming_pdfs_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(incoming_pdfs_path, filename)
            pdf_files.append(filepath)
    return pdf_files


def images_from_pdf(path):
    return convert_from_path(path)


def extract_text(images):
    all_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        all_text += text + "\n"
    return all_text


def write_text_file(directory, filename, text):
    with open(f'{directory}{filename}.txt', 'w') as f:
        f.write(text)

def slice_text(all_text):
    # find the start and end of the desired sections
    start1 = all_text.find("\n\nSUMMARY OF KEY INFORMATION\n\n")
    end1 = all_text.find("\n\n42. Attachments. We will provide you with")
    start2 = all_text.find("DOCUMENT AUDIT\n\n")

    # error checking
    if start1 == -1 or end1 == -1 or start2 == -1:
        print(f"Error: Could not find all required strings in the text.")
        return None

    # extract the desired sections
    text1 = all_text[start1:end1]
    text2 = all_text[start2:]

    # # remove duplicate lines from the second section
    # lines = text2.split('\n')
    # unique_lines = list(dict.fromkeys(lines))  # this removes duplicates while preserving order
    # text2_unique = '\n'.join(unique_lines)

    return text1 + "\n" + text2
    
def read_pdfs(incoming_pdfs_path):
    paths = only_pdfs(incoming_pdfs_path)

    for path in paths:
        filename = os.path.splitext(os.path.basename(path))[0]
        print(f'Extracting data for {filename}')
        
        directory = 'data_ingest/processed_text_files/'
        os.makedirs(directory, exist_ok=True)

        images = images_from_pdf(path)
        all_text = extract_text(images)
        select_text = slice_text(all_text)
        
        write_text_file(directory, filename, select_text)

    return select_text


if __name__ == "__main__":
    incoming_pdfs_path = 'data_ingest/incoming_pdfs/'
    read_pdfs(incoming_pdfs_path)
