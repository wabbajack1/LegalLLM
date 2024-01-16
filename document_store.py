from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings


from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from clean_documents import cleanup_documents
from split_documents import get_documents_splitted

DOCUMENT_PATH = "./raw-documents"
FIXED_DOCUMENT_PATH = "./fixed-documents"

ollama_embeddings = OllamaEmbeddings(base_url='http://vps.janmd.de:11434', model="phi")


def get_chroma() -> Chroma:
    store = LocalFileStore("./cache/")

    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        ollama_embeddings, store, namespace=ollama_embeddings.model
    )

    cleanup_documents(DOCUMENT_PATH, FIXED_DOCUMENT_PATH)

    documents = get_documents_splitted(FIXED_DOCUMENT_PATH)
    print(f"Loading {len(documents)} documents into chroma store. Can take some time.")

    return Chroma.from_documents(documents, cached_embedder, persist_directory="./chroma_db")
