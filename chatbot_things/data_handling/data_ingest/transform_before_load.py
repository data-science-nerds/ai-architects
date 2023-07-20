import os
import re
import json
# from data_cleanse.str_delimiters import slice_dict
# from ...data_handling.data_cleanse.str_delimiters import slice_dict
from str_delimiters import slice_dict

from pprint import pprint

# from ...utilities.relative_paths import directory_path_already_to_text

# directory_path_already_to_text = '../ai-architects/chatbot_things/data_handling/data_ingest/processed_text_files' 


def decisions(stripped_str):
    split_values = stripped_str.split("OR")

    right_answer = None
    for value in split_values:
        trimmed_value = value.strip()
        if '0' not in trimmed_value:
            right_answer = trimmed_value
            break
        elif '&' in trimmed_value:
            right_answer = trimmed_value
            break
        else:
            right_answer = 'NA'
    right_answer = right_answer.replace('&', '')
    parsed_dict = {'refund check': right_answer}
    return parsed_dict


def parse_signed_value(dictionary):
    if 'signed' in dictionary:
        value = dictionary['signed']
        if value is not None:
            # Apply the desired logic to the 'signed' value
            # For example, splitting it based on a specific pattern
            parsed_value = value.split("\n")[0].strip()

            # Update the dictionary with the parsed value
            dictionary['signed'] = decisions(parsed_value)

    return dictionary


def strip_spaces_and_newlines_in_dict(d):
    res =  {
        k.strip().replace('\n', ''): v.strip().replace('\n', '') if isinstance(v, str) else v
        for k, v in d.items()
    }
    return res


def clean_string(s):
    """Remove leading/trailing spaces and newline characters from a string."""
    return s.strip().replace('\n', '')


def clean_dictionary(d):
    """Clean all keys and values in a dictionary."""
    clean_dict = {clean_string(k): clean_string(v) for k, v in d.items() if isinstance(v, str)}
    return clean_dict


def extract_substrings(text):
    parts = text.split("DOCUMENT AUDIT", 1)
    if len(parts) == 2:
        second_half = parts[1]
        matches = re.findall(r'(?:signed|dated) ((?!Act|\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} [AP]MCDT).*?)(?: addendum| lease)', second_half, re.IGNORECASE)
        return ', '.join(matches)
    return ''


def process_dictionary(d):
    """
    Apply the extract_substrings function to the value of the key "signed" when it contains the word "AUDIT."
    """
    for k, v in d.items():
        if k == "signed" and "AUDIT" in v:
            d[k] = extract_substrings(v)
    return d


def pretty_print(d):
    """Print a dictionary in a pretty, easy-to-read format."""
    print(json.dumps(d, indent=4, sort_keys=True))


def clean_value(key, value):
    """
    This helper function cleans the given value based on the key.
    """
    drop_chars = ['Unit #', '@', '$#', 'H', '$$', '$', 'B Initial late fee (Par. 6) §_ 126.00 or']
    starts_with = ['(Par. 5) for', '%', 'staying more than__']

    for char in drop_chars:
        if value.endswith(char):
            value = re.sub(re.escape(char) + r'\Z', '', value)

    for start_ in starts_with:
        if value.startswith(start_):
            value = re.sub(re.escape(start_) + r'\A', '', value)

    if key == 'Address':
        if value.endswith('Unit #'):
            value = value.replace('Unit #', '')
    elif key == 'animal rent' and value == '$':
        value = 'pets not authorized'
    elif key == 'termination notice':
        value = value.replace('&', ' days')
    elif value == '':
        value = 'NA'
    elif ' OR ' in value:
        values = value.split(' OR ')
        for val in values:
            if '0' not in val:
                value = val
                break
    return value


def shorten_str_to_dict(txt)-> dict:
    """
    This function receives a string and a dictionary with slice information,
    and returns a new dictionary with the sliced strings.
    """
    txt_to_dict = {}
    for key, (start_marker, end_marker) in slice_dict.items():
        start = txt.find(start_marker)
        if start != -1: # Ensure start marker was found
            start += len(start_marker)
            if end_marker is None: # Check if end marker is None
                txt_to_dict[key] = txt[start:] # If it is, take the rest of the text from the start index
            else:
                end = txt.find(end_marker, start) # Search for the end marker starting from the end of the start marker
                if end != -1: # Ensure end marker was found
                    txt_to_dict[key] = txt[start:end] # Exclude the start and end markers from the slice
        if key == "signed" and "AUDIT\n\n" in txt_to_dict:
            txt_to_dict[key] += txt[txt.find("AUDIT\n\n") + len("AUDIT"):] # Append everything from "Manager" onwards until the end of the document
    # print(f'output from shorten_str: {txt_to_dict}\n{type(txt_to_dict)}')
    return txt_to_dict


def clean_ammendments(ammendments_str: str) -> str:
    """Reduce ammendments to only necessary ones."""
    if not isinstance(ammendments_str, str):
        print("Error: Expected str but received: ", type(ammendments_str))
        return []
    # print(ammendments_str)
    signed_ammendments = []
    # for amendment in ammendments_str:
    if 'signed' in ammendments_str:
        signed_ammendments = ammendments_str.split(':')
    # return signed_ammendments
    signed = []
    for str_ in signed_ammendments:
        if 'signed' in str_ and 'documents' not in str_ and 'DOCUMENT' not in str_:
            str_ = str_.split("signed")[1]
            signed.append(str_)
    
    # drop any dates
    list_without_dates = [item.rsplit(' ', 3)[0] for item in signed]
    
    # keep only unique items
    my_set = set(list_without_dates)

    # If you need a list again, you can convert it back
    unique_list = list(my_set)

    return unique_list




def slice_dict_strings(shortened_dict: dict) -> dict:
    """
    This function receives a string and returns a new dictionary with the sliced and cleaned strings.
    """

    # Clean the value based on the key
    for key, value in shortened_dict.items():
        shortened_dict[key] = clean_value(key, value)
    # pprint(shortened_dict)

    # Rename the "signed" key to "ammendments"
    if 'signed' in shortened_dict:
        shortened_dict['ammendments'] = shortened_dict['signed']
        del shortened_dict['signed']
    return shortened_dict