import os

import re

def sanitize_filename(filename: str) -> str:
    '''Keep only valid chars.'''
    # Split the filename into base name and extension
    basename, extension = os.path.splitext(filename)

    # Convert base name to lowercase and replace spaces and hyphens with underscores
    new_basename = basename.lower().replace(' ', '_').replace('-', '_').replace('__', '_')

    # Remove any characters that are not letters, numbers, or underscores
    new_basename = re.sub(r'[^a-zA-Z0-9_]', '', new_basename)

    # Combine the sanitized base name with the original extension
    new_filename = new_basename + extension

    return new_filename

def rename_files(directory: str) -> bool:
    '''Clean up all file names'''
    new_filename: str = ''
    for filename in os.listdir(directory):
        try:
            # create new filename
            new_filename = sanitize_filename(filename)
        except EOFError:
            print(f'ALERT!!  Error reading in file {filename}')
            return False
        # rename file
        os.rename(
            os.path.join(directory, filename), 
            os.path.join(directory, new_filename)
        )
    print('all files renamed')
    return True
