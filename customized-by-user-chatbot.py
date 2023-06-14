# ! git clone https://github.com/irina1nik/context_data.git
# ! git clone https://github.com/elsaVelazquez/context_data
import git
import os
import shutil

repo_dir = "context_data"
if os.path.exists(repo_dir):
    shutil.rmtree(repo_dir)  # Removes the directory and all its contents

git.Git(".").clone("git@github.com:data-science-nerds/context_data.git")


# !pip install llama-index==0.5.6
# !pip install langchain==0.0.148
import subprocess
subprocess.check_call(["pip", "install", "llama-index==0.5.6"])
subprocess.check_call(["pip", "install", "langchain==0.0.148"])

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
api_key = os.getenv("GPT_KEY")


from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
from IPython.display import Markdown, display

def construct_index(directory_path):
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
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    index.save_to_disk('index.json')

    return index

def ask_ai():
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    while True:
        query = input("What do you want to ask? ")
        response = index.query(query)
        display(Markdown(f"Response: <b>{response.response}</b>"))

# os.environ["OPENAI_API_KEY"] = input("run the cell then paste your key into the input box")
api_key = 'your key here'
os.environ["OPENAI_API_KEY"] = api_key

construct_index("context_data/data")

# colab_venv = ! pip freeze
# colab_venv


ask_ai()


