import os
import logging

import langchain
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAI
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware


from crawler import crawl_and_store
from document_store import get_faiss
from template_prompt import Legal_Template

logging.basicConfig(format='[%(levelname)s] :%(message)s',
                    level=logging.DEBUG if os.getenv('VERBOSE') == "True" else logging.INFO)

# Load settings from the .env file
load_dotenv()

langchain.verbose = os.getenv('VERBOSE') == "True"


def get_model(base_url: str, model_name: str = "mistral"):
    """
    Get the LLM that is used.
    When the model is "open-ai" we will use the GPT3.5 model by OpenAI
    Otherwise try to access a local model that is running
    on the private machine using Ollama https://github.com/ollama/ollama

    :param base_url: If an Ollama model is used this endpoint will be queried.
    :param model_name: The name of the model that will be passed to Ollama.
    :return: LangChain LLM model
    """
    if model_name == "open-ai":
        return OpenAI()

    ollama = Ollama(base_url=base_url, model=model_name)
    return ollama


if __name__ == "__main__":
    # Check if env file exists. Otherwise, copy the example and exit with an error to modify the file.
    if not os.path.exists(".env"):
        logging.error("Please copy the .env.example file to .env and configure it.")
        exit(1)

    # Check if the document path exists. Otherwise, create it.
    # Also check if the fixed document path exists. Otherwise, create it.
    # Also check if any documents are in the document path
    if not os.path.exists(os.getenv("DOCUMENT_PATH")) or not os.listdir(os.getenv("DOCUMENT_PATH")):
        if not os.path.exists(os.getenv("DOCUMENT_PATH")):
            logging.warning(f"Document path {os.getenv('DOCUMENT_PATH')} does not exist. Creating it.")
            os.makedirs(os.getenv("DOCUMENT_PATH"))

        logging.warning(f"Document path {os.getenv('DOCUMENT_PATH')} is empty. Crawling documents.")
        crawl_and_store(
            start_legislation=os.getenv("START_LEGISLATION", "CELEX:32020R0852"),
            metadata=os.getenv("METADATA", "crawled_data.json"),
            html_dir=os.getenv("DOCUMENT_PATH"),
            max_depth=int(os.getenv("MAX_DEPTH", "2"))
        )

        logging.info(f"Finished crawling documents. Crawled {len(os.listdir(os.getenv('DOCUMENT_PATH')))} documents.")

    # get the LLM
    model = get_model(os.getenv("MODEL_URL"), os.getenv("MODEL"))
    logging.info(f"Starting LegalLLM using {os.getenv('MODEL')} as LLM.")

    # choose task
    tasks_retriever = Legal_Template()
    task_template = tasks_retriever.task1_template()

    template = """
        Answer the question based only on the following context:
        {context}

        Question: {question}

        If you know the answer, give only the Articles numbers as an answer.
        If you dont know the answer based on the context, respond with "I dont know."
        Don't make up an answer.
        """

    # init task
    prompt = PromptTemplate.from_template(template)

    chain = (
            {"context": get_faiss().as_retriever(search_type="mmr"), "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
    )

    app = FastAPI(
        title="LegalLLM API",
        version="1.0",
        description="API for LegalLLM.",
    )

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    add_routes(
        app,
        chain,
        path="/legal",
    )

    uvicorn.run(app, host="localhost", port=8000)

    """
    An economic activity that pursues the environmental objective of climate change mitigation should contribute substantially to 
    the stabilisation of greenhouse gas emissions by avoiding or reducing them or by enhancing greenhouse gas removals. The economic activity 
    should be consistent with the long-term temperature goal of the Paris Agreement. That environmental objective should be interpreted in accordance 
    with relevant Union law, including Directive 2009/31/EC of the European Parliament and of the Council.
    """
    # print(chain.invoke("What assets are in scope of Taxonomy-eligibility reporting for financial undertakings?"))