from document_store import get_chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from template_prompt import Legal_Template
import langchain




langchain.verbose = True
# langchain.debug = True

def get_model(base_url:str, model_name:str="mistral"):
    ollama_embeddings = OllamaEmbeddings(base_url=base_url, model=model_name)
    ollama = Ollama(base_url=base_url, model=model_name)
    return ollama

if __name__ == "__main__":

    model = get_model("http://127.0.0.1:11434")
    
    # choos task
    tasks_retriever = Legal_Template()
    task_template = tasks_retriever.task1_template()

    template = """
        Answer the question based only on the following context:
        {context}

        Question: {question}

        If you know the answer, give only the Articles numbers as an answer.
        If you dont know the answer based on the context, respond with "I dont know."
        Don't make up an answer.
        """
    
    # init task
    prompt = PromptTemplate.from_template(template)

    chain = (
        {"context": get_chroma().as_retriever(search_type="mmr"), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    """
    An economic activity that pursues the environmental objective of climate change mitigation should contribute substantially to 
    the stabilisation of greenhouse gas emissions by avoiding or reducing them or by enhancing greenhouse gas removals. The economic activity 
    should be consistent with the long-term temperature goal of the Paris Agreement. That environmental objective should be interpreted in accordance 
    with relevant Union law, including Directive 2009/31/EC of the European Parliament and of the Council.
    """
    print(chain.invoke("What assets are in scope of Taxonomy-eligibility reporting for financial undertakings?"))