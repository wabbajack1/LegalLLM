from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

ollama_embeddings = OllamaEmbeddings(base_url='http://vps.janmd.de:11434', model="phi")
ollama = Ollama(base_url='http://vps.janmd.de:11434', model="phi")


def get_embeddings(text):
    return ollama_embeddings.embed_query(text)


def print_query_stream(query):
    for chunk in ollama.stream(query):
        print(chunk, end="", flush=True)


if __name__ == '__main__':
    print(get_embeddings("Hello world!"))

    print_query_stream("Hello world!")
