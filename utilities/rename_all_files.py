import os


def rename_files(directory: str) -> bool:
    '''Clean up all file names'''
    for filename in os.listdir(directory):
        try:
            # create new filename
            new_filename = filename.lower().replace(' ', '_').replace('-', '_')
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
