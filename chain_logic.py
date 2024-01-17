from document_store import get_chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from template_prompt import Legal_Template
import langchain




langchain.verbose = True
langchain.debug = True

def get_model(base_url:str, model_name:str="phi"):
    ollama_embeddings = OllamaEmbeddings(base_url=base_url, model=model_name)
    ollama = Ollama(base_url=base_url, model=model_name)
    return ollama

if __name__ == "__main__":

    model = get_model("http://localhost:11434")
    
    # choos task
    tasks_retriever = Legal_Template()
    task_template = tasks_retriever.task1_template()

    template = """Answer the question based only on the following context. If you do not
        know the answer or want to generate your answer based on your model, respond by saying "I do not know.":
        {context}

        Question: {question}
        """
    
    # init task
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": get_chroma().as_retriever(), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    print(chain.invoke("What is Green house gas emission?"))