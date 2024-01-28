import os
import logging

from dotenv import load_dotenv
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import _import_faiss
from langchain_openai import OpenAIEmbeddings

from clean_documents import cleanup_documents
from split_documents import get_documents_splitted

# Load settings from the .env file
load_dotenv()

FAISS = _import_faiss()

DOCUMENT_PATH = os.getenv("DOCUMENT_PATH")
FIXED_DOCUMENT_PATH = os.getenv("FIXED_DOCUMENT_PATH")


def get_faiss(model_name: str = 'mistral') -> FAISS:
    """
    Clean and pre-process data and store it into the vector database for later retrieval.

    :param model_name: The name of the LLM that will be used to create the embeddings.
    :return: FAISS vector database
    """
    ollama_embeddings = OllamaEmbeddings(base_url=os.getenv("MODEL_URL"), model=os.getenv("MODEL"))
    open_ai_embeddings = OpenAIEmbeddings()

    embeddings = ollama_embeddings if model_name == 'ollama' else open_ai_embeddings

    store = LocalFileStore("./cache/")
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        embeddings, store, namespace=embeddings.model
    )

    # Pre-Process the documents before splitting
    cleanup_documents(DOCUMENT_PATH, FIXED_DOCUMENT_PATH)

    # Split the documents using the langchain html splitter
    documents = get_documents_splitted(FIXED_DOCUMENT_PATH)
    logging.info(f"Loading {len(documents)} documents into FAISS store. Can take some time.")

    return FAISS.from_documents(documents, cached_embedder)
