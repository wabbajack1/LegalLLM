import requests
from bs4 import BeautifulSoup
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# summerizer
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

    ollama = Ollama(base_url=base_url, model=model_name)
    return ollama


def get_raw_qa(url:str):
    """Gets qa html page, and turns into json.

    Args:
        url (str): url

    Returns:
        qa_json: key=question, value=answer 
    """
    # URL of the webpage you want to scrape
    url = url

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        qa_pairs = []

        # Find all question elements
        questions = soup.find_all(class_="oj-ti-grseq-1")

        # Loop through all found questions
        for question in questions:
            
            if question.get_text(strip=True)[-1] != "?":
                continue

            # Initialize a list to hold all parts of the answer
            answer_parts = []
            # Get the immediate next sibling of the question, which should be the answer paragraph
            answer_p = question.find_next_sibling(class_="oj-normal")
            while answer_p:
                # If this sibling is a paragraph, add its text to the answer_parts list
                answer_parts.append(answer_p.get_text(strip=True))
                # If this sibling is a table, extract all its text
                if answer_p.find_next_sibling('table'):
                    table = answer_p.find_next_sibling('table')
                    # Extract text from all table cells
                    table_text = ' '.join(cell.get_text(strip=True) for cell in table.find_all(['td', 'th']))
                    answer_parts.append(table_text)
                    # Move to the next element after the table
                    answer_p = table.find_next_sibling(class_="oj-normal")
                else:
                    # If no table follows, just move to the next sibling paragraph
                    answer_p = answer_p.find_next_sibling(class_="oj-normal")
            
            # Combine all parts of the answer into one string
            full_answer = ' '.join(answer_parts)

            # Append the question and its full answer to the list
            qa_pairs.append({
                'question': question.get_text(strip=True)[3:],
                'answer': full_answer
            })
    else:
        print(f"Failed to retrieve the webpage, status code: {response.status_code}")
        return None

    return qa_pairs

if __name__ == "__main__":

    # model for summery
    model = get_model("http://127.0.0.1:11434")

    url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:C_202300305'

    # get qa dict
    qa_pairs = get_raw_qa(url)
    
    print(qa_pairs)

    print(20*"-")

    for qa_dict in qa_pairs:
        prompt = PromptTemplate.from_template("You are a expert summarizer,  summarizer the next text: {input}?")
        chain = (
                {"input": RunnablePassthrough()}
                | prompt
                | model
                | StrOutputParser()
            )
        llm_answer = chain.invoke(qa_dict["answer"])
        qa_dict["answer"] = llm_answer

        print(qa_dict["question"], "--->", llm_answer, "----", qa_dict["answer"])

    qa_json = json.dumps(qa_pairs, ensure_ascii=False, indent=2)

    # File path to save the JSON
    file_path = 'eval_data/qa_data.json'

    # Writing the JSON data to a file
    with open(file_path, 'w') as json_file:
        json_file.write(qa_json)





