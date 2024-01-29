import requests
from bs4 import BeautifulSoup
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

def crawl_eurlex(url, save_dir, filename):
    try:
        # Send a request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for request success

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the relevant information
        paragraphs = soup.find_all('p')
        text = '\n'.join([para.get_text() for para in paragraphs])

        # Save the text in a file in the specified directory
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(os.path.join(save_dir, filename), 'w', encoding='utf-8') as file:
            file.write(text)

        return f"Text saved to {os.path.join(save_dir, filename)}"
    except Exception as e:
        return str(e)

url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32021R2178"
save_directory = 'fixed-documents'
file_name = 'disclosure_delegated_act.txt'
result = crawl_eurlex(url, save_directory, file_name)


text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=3000,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

with open("fixed-documents/disclosure_delegated_act.txt") as f:
    state_of_the_union = f.read()
    
texts = text_splitter.create_documents([state_of_the_union])
print(len(texts[:50]))



