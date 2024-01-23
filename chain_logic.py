import langchain
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAI


from document_store import get_document_store
from template_prompt import Legal_Template

langchain.verbose = True
langchain.debug = True


def get_model(base_url: str, model_name: str = "phi"):
    if model_name == "open-ai":
        return OpenAI()

    ollama_embeddings = OllamaEmbeddings(base_url=base_url, model=model_name)
    ollama = Ollama(base_url=base_url, model=model_name)
    return ollama


if __name__ == "__main__":
    model = get_model("http://localhost:11434", model_name="open-ai")

    # choose task
    tasks_retriever = Legal_Template()
    task_template = tasks_retriever.task1_template()

    template = """Answer the question based only on the following context. If you do not
        know the answer or want to generate your answer based on your model, respond by saying "I do not know.":
        {context}

        Question: {question}
        """

    retriever = get_document_store(model_name="open-ai").as_retriever()

    # init task
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
    )

    # print(chain.invoke("How can companies contribute substantially to climate change mitigation?"))
    print(chain.invoke("What are environmental objectives provided by the EU taxonomy?"))
