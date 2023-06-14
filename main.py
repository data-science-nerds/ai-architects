from utilities.rename_all_files import rename_files
from data_ingest.incoming_pdf_to_text import read_pdfs

incoming_pdfs_path = 'data_ingest/incoming_pdfs' #/Users/elsa/Documents/CODE/aiarchitects/data-science-nerds/ai-architects/data_ingest/incoming_pdfs'

if __name__ == '__main__':
    renamed = False
    to_pdf = False
    
    # clean up all pdf file names
    renaed = rename_files(incoming_pdfs_path)
    
    # read in pdf as text + imgs
    to_pdf = read_pdfs(incoming_pdfs_path)
    
    