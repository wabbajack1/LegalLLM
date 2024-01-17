from document_store import get_chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from template_prompt import Legal_Template

def get_model(base_url:str, model_name:str="phi"):
    ollama_embeddings = OllamaEmbeddings(base_url='localhost:11434', model=model_name)
    ollama = Ollama(base_url='localhost:11434', model=model_name)
    return ollama

if __name__ == "__main__":

    model = get_model()
    
    # choos task
    tasks_retriever = Legal_Template()
    task_template = tasks_retriever.task1_template()



    # init task
    prompt = ChatPromptTemplate.from_template(task_template)
    chain = (
        {"context": get_chroma(), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
