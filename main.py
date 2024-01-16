from document_store import get_chroma

if __name__ == '__main__':
    chroma = get_chroma()

    query = "What is greenhouse gas?"

    docs = chroma.similarity_search(query)
    print(docs[0].page_content)
