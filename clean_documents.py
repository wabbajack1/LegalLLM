import os
import re

from bs4 import BeautifulSoup


def remove_non_alphanumeric_spaces(input_string):
    input_string = input_string.replace('\u00A0', ' ')

    # Use regular expression to replace non-alphanumeric spaces
    result = re.sub(r'\s+(?![\w()\"\'])', '', input_string)
    return result


def cleanup_documents(target_dir: str, output_dir: str):
    """
    Takes the raw input from https://eur-lex.europa.eu/ and cleans up some stuff.

    :param target_dir: directory from where to load the files to be cleaned
    :param output_dir: directory where the cleaned files will be stored
    :return: nothing
    """
    raw_html_files = os.listdir(target_dir)

    for raw_html_file in raw_html_files:
        with open(f"{target_dir}/{raw_html_file}", 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the element with class "eli-container"
        eli_container = soup.find(class_='eli-container')

        # Check if the element was found
        if eli_container:
            # Find all elements with class "oj-ti-art" within the "eli-container" subtree
            for tag in eli_container.find_all(class_='oj-ti-art'):
                new_tag = soup.new_tag('h1')
                new_tag.string = tag.string
                tag.replace_with(new_tag)

            # Save the modified HTML content to the output file within the "eli-container" subtree
            with open(f"{output_dir}/{raw_html_file}", 'w', encoding='utf-8') as file:
                html_output = eli_container.prettify()
                html_output = html_output.replace("\r\n", "")
                html_output = html_output.replace("\n", "")
                html_output = html_output.replace('‘', ' "')
                html_output = html_output.replace('’', ' "')
                html_output = html_output.replace('“', '\'')
                html_output = html_output.replace('”', '\'')

                html_output = remove_non_alphanumeric_spaces(html_output)

                file.write(html_output)
        else:
            print('Element with class "eli-container" not found in the document.')
