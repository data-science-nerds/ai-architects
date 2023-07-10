import re
import json
# from pprint import pprint
from str_delimiters import slice_dict


def decisions(stripped_str):
    split_values = stripped_str.split("OR")

    right_answer = None
    for value in split_values:
        trimmed_value = value.strip()
        if not trimmed_value.startswith('0'):
            right_answer = trimmed_value
            break

    parsed_dict = {'refund check': right_answer}
    return parsed_dict


def parse_signed_value(dictionary):
    if 'amendments' in dictionary:
        value = dictionary['amendments']
        if value is not None:
            # Apply the desired logic to the 'signed' value
            # For example, splitting it based on a specific pattern
            parsed_value = value.split("\n")[0].strip()

            # Update the dictionary with the parsed value
            dictionary['amendments'] = decisions(parsed_value)

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


def slice_string(txt):
    """
    This function receives a string and a dictionary with slice information,
    and returns a new dictionary with the sliced strings.
    """
    sliced_txt = {}
    for key, (start_marker, end_marker) in slice_dict.items():
        start = txt.find(start_marker)
        if start != -1: # Ensure start marker was found
            start += len(start_marker)
            if end_marker is None: # Check if end marker is None
                sliced_txt[key] = txt[start:] # If it is, take the rest of the text from the start index
            else:
                end = txt.find(end_marker, start) # Search for the end marker starting from the end of the start marker
                if end != -1: # Ensure end marker was found
                    sliced_txt[key] = txt[start:end] # Exclude the start and end markers from the slice
        # import pdb; pdb.set_trace()
        if key == "amendments" and "AUDIT" in sliced_txt:
            sliced_txt[key] += txt[txt.find("AUDIT") + len("AUDIT"):] # Append everything from "Manager" onwards until the end of the document
    return sliced_txt


def cleanse_text(txt):
    sliced_txt = slice_string(txt, slice_dict)
    
    # Apply cleaning, extraction, and processing functions
    clean_dict = clean_dictionary(sliced_txt)
    # import pdb; pdb.set_trace()
    processed_dict = process_dictionary(clean_dict)
    # import pdb; pdb.set_trace()
    # Convert dictionary back to a single string
    stripped_str = strip_spaces_and_newlines_in_dict(processed_dict)
    decision_str = parse_signed_value(stripped_str)
    return decision_str  #final_string



if __name__ == "__main__":
    # clean up this text, right now making it to decisions
    # probably easier to do as:
    ammendmas = []
    if 'no smoking':
        ammendmas.append('no smoking, ')
    txt = "{'Address': '10956 Dizzy Dean PlaceUnit #', 'beginning date': '11/01/2020@', 'termination notice': '30& Total', 'security deposit 1': '$ 1050.00H', 'end date': '10/31/2021H', 'guest stays': 'staying more than__7___days', 'pet deposit': '$ 200.00', 'pet security deposit': '0 does OR & does not include an animal deposit.', 'refund check': '& one check jointly payable to all residents (default),ORO one check payable to and mailed to@', 'keys/ access': '(Par. 5) for_2 unit, mailbox,other# Your move-out notice', 'included in rent': '0 garage, 0 storage, 0) carport, 0 washer/dryer, or 0 other#', 'total rent': '$ 1050.00', 'begin late fee': '3rdB Initial late fee (Par. 6) §_ 126.00 or', 'bounced check': '$ 25.00', 'animal rent': '$', 'pest control': '$$@', 'repairman': '50.00', 'prorated': 'O first month ORO secondmonth $', 'daily late fee': '$', 'animal violation': 'Initial $ 100.00 Daily $#', 'trash': '', 'replace trash can': '% you OR Ous', 'chatbot_things/utilities': '$ 50.00', 'reletting': '$ 892.50', 'insurance': '& required to buy insurance OR© not required to buy insurance', 'provisions': 'Kitchen range is property of and is provided to Resident by Owner.', 'signed': {'refund check': 'Mold Information and Prevention, Limited Waiver of Rights and Protections Under the U.S. Servicemembers Civil Relief Act19 10/16/20 09:28:32 PMCDT Alex Otos checked box on No Smoking, No Smoking, documents22 10/16/20 09:59:06 PM CDT Michael Jones signed Bed Bug, Bed Bug, Insurance, Residential, Residential, Mold Information and Prevention, Mold Information and Prevention, Limited Waiver of Rights and Protections Under the U.S. Servicemembers Civil Relief Act38 10/16/20 09:59:06 PMCDT Michael Jones signed No Smoking'}}"

    clean_text = cleanse_text(txt)
