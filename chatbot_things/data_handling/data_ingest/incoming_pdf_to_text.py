import os
from pdf2image import convert_from_path
import pytesseract
from pprint import pprint

from transform_before_load import (
    slice_dict_strings,
    clean_dictionary,
    process_dictionary,
    strip_spaces_and_newlines_in_dict,
    parse_signed_value,
    shorten_str_to_dict,
    clean_ammendments,
)


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

    return text1 + "\n" + text2


def cleanse_text(txt):
    '''Apply python automation to format LLM's CONTEXT.'''
    # Convert scraped text  to dictionary
    shortened_to_dict0 = shorten_str_to_dict(txt)
    # 
    shortened_to_dict = strip_spaces_and_newlines_in_dict(shortened_to_dict0)
    sliced_dict = slice_dict_strings(shortened_to_dict)
    # Apply cleaning, extraction, and processing functions
    clean_dict = clean_dictionary(sliced_dict)
    processed_dict = process_dictionary(clean_dict)
    # Convert dictionary back to a single string
    stripped_dict = strip_spaces_and_newlines_in_dict(processed_dict)
    decision_dict = parse_signed_value(stripped_dict)
    
    # keep only relevant ammendments
    if 'ammendments' in decision_dict.keys():
        # Get the "ammendments" value from the dictionary
        ammendments_str = decision_dict.get('ammendments')

        # Clean the ammendments string
        cleaned_ammendments = clean_ammendments(ammendments_str)
        # Update the dictionary with the cleaned ammendments
        decision_dict['ammendments'] = cleaned_ammendments
    
    # Sufficient security because resides in the cloud and 
    # would minimally require pem keys to intercept, 
    # which is not likely for a demo
    if 'Address' in decision_dict.keys():
        decision_dict["Address"] = "removed for security"
    
    # put back into string format
    return str(decision_dict)  #final_string


def read_pdfs(incoming_pdfs_path):
    paths = only_pdfs(incoming_pdfs_path)

    for path in paths:
        filename = os.path.splitext(os.path.basename(path))[0]
        print(f'Extracting data for {filename}')

        directory = 'chatbot_things/data_handling/data_ingest/processed_text_files/'
        os.makedirs(directory, exist_ok=True)

        images = images_from_pdf(path)
        all_text = extract_text(images)
        
        select_text = slice_text(all_text)
        cleaned_text = cleanse_text(select_text)
        print(cleaned_text)
        write_text_file(directory, filename, cleaned_text)

    return cleaned_text


if __name__ == "__main__":
    incoming_pdfs_path = 'chatbot_things/data_handling/data_ingest/incoming_pdfs/'
    read_pdfs(incoming_pdfs_path)
