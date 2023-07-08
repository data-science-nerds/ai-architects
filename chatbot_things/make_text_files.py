from chatbot_things.utilities.rename_all_files import rename_files
from chatbot_things.data_handling.data_ingest.incoming_pdf_to_text import read_pdfs
from chatbot_things.data_handling.data_cleanse.make_priming import cleanse_text

incoming_pdfs_path = 'chatbot_things/data_handling/data_ingest/incoming_pdfs' #/Users/elsa/Documents/CODE/aiarchitects/data-science-nerds/ai-architects/chatbot_things/data_handling/data_ingest/incoming_pdfs'

if __name__ == '__main__':
    renamed = False
    to_pdf = False
    
    # clean up all pdf file names
    renamed = rename_files(incoming_pdfs_path)
    
    # read in pdf as text + imgs
    to_text = read_pdfs(incoming_pdfs_path)

    clean_text = cleanse_text(to_text)