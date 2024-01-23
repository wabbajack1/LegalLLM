from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import _import_faiss
from langchain_openai import OpenAIEmbeddings

from clean_documents import cleanup_documents
from split_documents import get_documents_splitted

FAISS = _import_faiss()

DOCUMENT_PATH = "./raw-documents"
FIXED_DOCUMENT_PATH = "./fixed-documents"

ollama_embeddings = OllamaEmbeddings(base_url='http://localhost:11434', model="phi")
open_ai_embeddings = OpenAIEmbeddings()


def get_document_store(model_name='ollama') -> FAISS:
    store = LocalFileStore("./cache/")

    embeddings = ollama_embeddings if model_name == 'ollama' else open_ai_embeddings

    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        embeddings, store, namespace=embeddings.model
    )

    cleanup_documents(DOCUMENT_PATH, FIXED_DOCUMENT_PATH)

    documents = get_documents_splitted(FIXED_DOCUMENT_PATH)
    print(f"Loading {len(documents)} documents into chroma store. Can take some time.")

    return FAISS.from_documents(documents, cached_embedder)
