from document_store import get_faiss
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from template_prompt import Legal_Template
import langchain
from langchain_openai import OpenAI



# langchain.verbose = True
# langchain.debug = True

def get_model(base_url:str, model_name:str="mistral"):
    ollama_embeddings = OllamaEmbeddings(base_url=base_url, model=model_name)
    ollama = ChatOllama(base_url=base_url, model=model_name)
    return ollama

def get_model(base_url: str, model_name: str = "mistral"):
    """
    Get the LLM that is used.
    When the model is "open-ai" we will use the GPT3.5 model by OpenAI
    Otherwise try to access a local model that is running
    on the private machine using Ollama https://github.com/ollama/ollama

    :param base_url: If an Ollama model is used this endpoint will be queried.
    :param model_name: The name of the model that will be passed to Ollama.
    :return: LangChain LLM model
    """
    if model_name == "open-ai":
        return OpenAI()

    ollama = Ollama(base_url=base_url, model=model_name)
    return ollama

if __name__ == "__main__":

    model = get_model("http://127.0.0.1:11434")
    
    # choose task
    tasks_retriever = Legal_Template()
    task_template = tasks_retriever.task1_template()
    
    system = """
        You are an AI assistant for answering questions about about EU taxonomy law. 
        Use the given pieces of context and question-answer examples to answer the user's question. 
        If you don't know the answer, just say "I don't know the answer." 
        Don't make up an answer.
    """

    human = """
        Use the provided context extracted from relevant documents and the following 
        three question-answer examples about the EU taxonomy Laws to help you answer the fourth question at the end.

        If you don't know the answer based on the context, just say "I don't know the answer." Don't make up an answer.
        ----------------
        CONTEXT:
        {context}
        ----------------

        QUESTION: What is a Taxonomy-eligible economic activity?
        ANSWER:
        - Article 1(5) of the Disclosures Delegated Act defines an eligible economic activity as an activity that is described in the delegated acts adopted under Article 10(3), Article 11(3), Article 12(2), Article 13(2), Article 14(2) and Article 15(2) of the Taxonomy Regulation. 
        - More specifically, according to Article 1(5) of the Disclosures Delegated Act, an economic activity is eligible irrespective of whether it meets any or all of the technical screening criteria laid down in the Climate Delegated Act (and future delegated acts). Therefore, the fact that an economic activity is Taxonomy-eligible does not give any indication of the environmental performance and sustainability of that activity.
        --> Article 1.5 (Disclosures Delegated Act); Article 10.3, Article 11.3, Article 12.2, Article 13.2, Article 14.2 and Article 15.2 (Taxonomy Regulation)

        QUESTION: What are 'enabling' and 'transitional' economic activities in the context of Taxonomy-eligibility reporting?
        ANSWER: 
        - Articles 16 and 10(2) of the Taxonomy Regulation define enabling and transitional economic activities
        --> Article 16, Article 10.2 (Taxonomy Regulation)

        QUESTION: How to identify and report eligibility for adaptation-related economic activities?
        ANSWER:
        - Adaptation activities, i.e. activities including adaptation solutions in accordance with Article 11 (1)(a) of the Taxonomy Regulation.
        - Enabling economic activities, i.e. activities providing adaptation solutions in accordance with Article 11 (1)(b) of the Taxonomy Regulation.
        --> Article 11 1.a, Article 11 1.b (Taxonomy Regulation)

        QUESTION: {question}
        ANSWER:
        Let's think step by step and only answer based on the context, if you dont have an anwer, based on the context, just say "I don't know the answer."
        Stop right there with no additional information to the unrelated question.
        You must format your output as a JSON value that adheres to a given "JSON Schema" instance. The Format has a answer and articles key, based on the answer, where articels has only the type(str).
    """

    # init task
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("user", human)
    ])

    chain = (
            {"context": get_faiss().as_retriever(search_kwargs={"k": 2}), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    print(chain.invoke("What does checking the compliance with the TSC on the substantial contribution and the DNSH mean in practice?"))