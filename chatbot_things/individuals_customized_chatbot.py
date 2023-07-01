# ! git clone https://github.com/irina1nik/context_data.git
# ! git clone https://github.com/elsaVelazquez/context_data
import git
import os
import shutil
import subprocess

from dotenv import load_dotenv

from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
from IPython.display import Markdown, display

from chatbot_things.utilities.relative_paths import (
    directory_path_already_to_text,
    directory_path_incoming_pdfs,
)

repo_dir = "context_data"
if os.path.exists(repo_dir):
    shutil.rmtree(repo_dir)  # Removes the directory and all its contents

git.Git(".").clone("git@github.com:data-science-nerds/context_data.git")

# import subprocess
subprocess.check_call(["pip", "install", "llama-index==0.5.6"])
subprocess.check_call(["pip", "install", "langchain==0.0.148"])


load_dotenv()  # take environment variables from .env.
api_key = os.getenv("OPEN_API_KEY")
   

# directory_path = '/Users/elsa/Documents/CODE/aiarchitects/data-science-nerds/ai-architects/chatbot_things/data_handling/data_ingest/incoming_pdfs'
def construct_index(directory_path):
    '''Run models.'''
    # directory_path = '/Users/elsa/Documents/CODE/aiarchitects/data-science-nerds/ai-architects/chatbot_things/data_handling/data_ingest/processed_text_files'

    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.2, model_name="text-davinci-003", max_tokens=num_outputs))

    # Load the documents
    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    index.save_to_disk('index.json')

    return index, documents

# construct_index("context_data/data")


def ask_ai(documents):
    # print(f'should be feeding this into prompt: promp_prep')
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    while True:
        query = input("\n\nYOUR QUESTION? ")
        query = f'*** {documents} + {query}'
        response = index.query(query)
        # print(type(response)
        
        # print("Response:", response.response)
        print("***", response.response)
        # import pdb; pdb.set_trace()

        # print(repr(response))  # Print the representation of the response object
        # print(response)  # Print the response object itself

        # rent = response.get_metadata("total_rent")  # Assuming "total_rent" is the metadata field for rent value
        # if rent is not None:
        #     print("Total Rent:", rent)
        # else:
        #     print("Response:", response.response)


if __name__ == "__main__":
    # # Use this path to generate text files
    # directory_path_incoming_pdfs = '/Users/elsa/Documents/CODE/aiarchitects/data-science-nerds/ai-architects/chatbot_things/data_handling/data_ingest/incoming_pdfs'

    # # Use this path once the files are already made
    # directory_path_already_to_text = '/Users/elsa/Documents/CODE/aiarchitects/data-science-nerds/ai-architects/chatbot_things/data_handling/data_ingest/processed_text_files'

    index, documents = construct_index(directory_path_already_to_text)
    ask_ai(documents)
