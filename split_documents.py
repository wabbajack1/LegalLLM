import os
import re

from langchain.text_splitter import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter


def remove_non_alphanumeric_spaces(input_string):
    # Use regular expression to replace non-alphanumeric spaces
    result = re.sub(r'\s+(?![\w()\"\'])', '', input_string)
    return result


def get_documents_splitted(target_dir: str):
    """
    Loads all html files from the DOCUMENT_PATH
    directory into langchain documents.

    :param target_dir: Directory from where the html files are loaded
    :return: list of documents
    """
    headers_to_split_on = [('h1', 'Article')]
    chunk_size = 3000
    chunk_overlap = 0

    # splitter
    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    chunk_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # documents
    raw_html_files = os.listdir(target_dir)
    target_documents = []

    for raw_html_file in raw_html_files:
        print(raw_html_file)

        if "climate_delegated_act.txt" == raw_html_file:
            with open("fixed-documents/disclosure_delegated_act.txt") as f:
                state_of_the_union = f.read()
                texts = chunk_splitter.create_documents([state_of_the_union])
                target_documents += texts[:50]

        # Split first at every html heading
        html_header_splits = html_splitter.split_text_from_file(f"{target_dir}/{raw_html_file}")
        # The HTML splitter creates also for every single headline a document.
        # I think we don't need them, so I will remove it.
        html_header_splits_with_metadata = [document for document in html_header_splits if document.metadata]

        # Split again with a maximum chunk size
        chunked_splits = chunk_splitter.split_documents(html_header_splits_with_metadata)

        for split in chunked_splits:
            split.page_content = split.page_content.replace("\n", "")
            split.page_content = remove_non_alphanumeric_spaces(split.page_content)

        target_documents += chunked_splits

    return target_documents
