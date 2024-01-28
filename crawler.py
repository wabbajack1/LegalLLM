import shutil
import requests
import json
import os
import logging

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def crawl_and_store(start_legislation: str, metadata: str, html_dir: str, max_depth: int) -> None:
    """
    Crawls the EUR-Lex website and stores the HTML files in the html_dir.

    :param start_legislation: The legislation to start crawling from
    :param metadata: The metadata file to store the references to the HTML files
    :param html_dir: The directory to store the HTML files
    :param max_depth: The maximum depth to crawl
    :return: None
    """
    visited_urls = set()
    base_url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/'
    urls_to_visit = [(base_url + '?uri=' + start_legislation, 0)]  # Start with depth 0
    data_store = {}  # Dictionary to store URL and reference to HTML file

    # Clear the contents of the html_files directories
    if os.path.exists(html_dir):
        shutil.rmtree(html_dir)
    os.makedirs(html_dir)

    # Clear the contents of the crawled_data.json
    with open(metadata, 'w', encoding='utf-8') as file:
        json.dump(data_store, file, ensure_ascii=False, indent=4)

    while urls_to_visit:
        current_url, depth = urls_to_visit.pop(0)
        if current_url not in visited_urls:
            logging.info(f"Count: {len(visited_urls)} - Depth: {depth} | Crawling: {current_url}")
            try:
                response = requests.get(current_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Write the HTML content to a file
                    html_file_name = f"depth_{depth}_page_{len(visited_urls)}.html"
                    html_file_path = os.path.join(html_dir, html_file_name)
                    with open(html_file_path, 'w', encoding='utf-8') as file:
                        file.write(response.text)

                    # Storing references in the data store
                    data_store[current_url] = {
                        'html_file': html_file_name,
                    }

                    if depth < max_depth:
                        for link in soup.find_all('a'):
                            href = link.get('href')
                            if href and not href.startswith('#'):
                                transformed_url = None
                                if './' in href:
                                    query_string = urlparse(href).query
                                    uri_param = parse_qs(query_string).get('uri')
                                    if uri_param:
                                        transformed_url = base_url + '?uri=' + uri_param[0]
                                elif href.startswith('http'):
                                    transformed_url = href

                                if transformed_url and transformed_url not in visited_urls:
                                    urls_to_visit.append((transformed_url, depth + 1))

                    visited_urls.add(current_url)
                else:
                    logging.error(f"Failed to crawl {current_url}: HTTP Status Code {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to crawl {current_url}: {e}")

            # Limit
            if len(visited_urls) > 1000:
                break

            # Store the reference data
            with open(metadata, 'w', encoding='utf-8') as file:
                json.dump(data_store, file, ensure_ascii=False, indent=4)
