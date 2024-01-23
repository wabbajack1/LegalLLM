from document_store import get_document_store

if __name__ == '__main__':
    chroma = get_document_store()

    query = "What is greenhouse gas?"

    docs = chroma.similarity_search(query)
    print(docs[0].page_content)
