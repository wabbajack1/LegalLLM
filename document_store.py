from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import _import_faiss

from clean_documents import cleanup_documents
from split_documents import get_documents_splitted

FAISS = _import_faiss()

DOCUMENT_PATH = "./raw-documents"
FIXED_DOCUMENT_PATH = "./fixed-documents"

ollama_embeddings = OllamaEmbeddings(base_url='http://localhost:11434', model="mistral")


def get_chroma() -> FAISS:
    """Clean and pre-process data and store it into the vector database for later retrieval.

    Returns:
        FAISS: vector databse object
    """
    store = LocalFileStore("./cache/") # local file storage

    # wrap embedder around chache
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        ollama_embeddings, store, namespace=ollama_embeddings.model
    )

    # must me fixed, with better pre-processing @fix
    cleanup_documents(DOCUMENT_PATH, FIXED_DOCUMENT_PATH)

    documents = get_documents_splitted(FIXED_DOCUMENT_PATH)
    print(f"Loading {len(documents)} documents into chroma store. Can take some time.")

    return FAISS.from_documents(documents, cached_embedder)


if __name__ == "__main__":

    db = get_chroma()

    retriever = db.as_retriever(
        search_type="mmr"
    )

    docs = retriever.get_relevant_documents("What does geological storage?")
    print(docs)
