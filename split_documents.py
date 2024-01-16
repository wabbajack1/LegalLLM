import os

from langchain.text_splitter import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter


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
        # Split first at every html heading
        html_header_splits = html_splitter.split_text_from_file(f"{target_dir}/{raw_html_file}")
        # The HTML splitter creates also for every single headline a document.
        # I think we don't need them, so I will remove it.
        html_header_splits_with_metadata = [document for document in html_header_splits if document.metadata]

        # Split again with a maximum chunk size
        chunked_splits = chunk_splitter.split_documents(html_header_splits_with_metadata)

        target_documents += chunked_splits

    return target_documents
