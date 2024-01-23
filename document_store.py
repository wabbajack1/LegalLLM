from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import _import_faiss
from clean_documents import cleanup_documents
from split_documents import get_documents_splitted


FAISS = _import_faiss()

DOCUMENT_PATH = "./raw-documents"
FIXED_DOCUMENT_PATH = "./fixed-documents"

ollama_embeddings = OllamaEmbeddings(base_url='http://localhost:11434', model="phi")


def get_chroma() -> FAISS:
    store = LocalFileStore("./cache/")

    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        ollama_embeddings, store, namespace=ollama_embeddings.model
    )

    cleanup_documents(DOCUMENT_PATH, FIXED_DOCUMENT_PATH)

    documents = get_documents_splitted(FIXED_DOCUMENT_PATH)
    print(f"Loading {len(documents)} documents into chroma store. Can take some time.")

    return FAISS.from_documents(documents, cached_embedder, persist_directory="./faiss_db")
