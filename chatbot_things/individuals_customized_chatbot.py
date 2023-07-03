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


def cybersecurity_checks(question_count):
    if question_count > 10:
        print(f"Maximum number of {question_count} questions reached. Number of questions is restricted as a way to implement cybersecurity checks and keep your data safe.")
        return False
    return True


def ask_ai(question, index, documents, question_count):
    '''Ask chatGPT the question'''
    # Maintain cyber safety
    cyber_checks = True
    cyber_checks = cybersecurity_checks(question_count)
    
    if cyber_checks is False:
        return None
    
    query = f'*** {documents} + {question}'
    response = index.query(query)
    question_count += 1
    return response.response, question_count


if __name__ == "__main__":
    # # Use this path to generate text files
    # data-science-nerds/ai-architects/chatbot_things/data_handling/data_ingest/incoming_pdfs'

    # # Use this path once the files are already made
    # /data-science-nerds/ai-architects/chatbot_things/data_handling/data_ingest/processed_text_files'
    index, documents = construct_index(directory_path_already_to_text)

    question_count = 0
    # limit total questions to prevent DDOS attacks
    while question_count < 10:
        question = input("Ask a question: ")
        response, question_count = ask_ai(question, index, documents, question_count)
        print(response)
