import os
import time
from consts import USER_AGENT, WAIT_REQUEST_SEC
import requests
import logging
import datetime
from log_utils import setup_logging_download
from utils import page_title_to_filename

setup_logging_download()

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": USER_AGENT
}
DEFAULT_PARAMS = {
    "action": "query",
    "prop": "revisions",
    "rvprop": "content",
    "rvslots": "main",
    "format": "json",
    "formatversion": 2
}


def download_pages(titles: list[str], output_dir="data/wiki_pages") -> None:
    for i, title in enumerate(titles):
        print(f"{i}/{len(titles)}")
        
        if is_saved(output_dir, title):
            logging.warning(f"Page '{title}' already downloaded. Skipping.")
            continue

        download_page(title, output_dir)
        time.sleep(WAIT_REQUEST_SEC)

def is_saved(output_dir: str, title: str) -> bool:
    path = os.path.join(output_dir, f"{title}.txt")
    return os.path.exists(path)
    
def download_page(title: str, output_dir="data/wiki_pages") -> None:
    params = {
        **DEFAULT_PARAMS,
        "titles": title
    }
    response = requests.get(WIKI_API_URL, params=params, headers=HEADERS)
    data = response.json()

    try:
        page = data['query']['pages'][0]
        if "missing" in page:
            return
        
        wikitext = page['revisions'][0]['slots']['main']['content']
    except (KeyError, IndexError) as e: 
        logging.error(f"Error processing page '{title}': {e}")
        return
    
    save_overwrite(output_dir, title, wikitext)

def save_overwrite(output_dir: str, title: str, wikitext: str) -> None:
    path = os.path.join(output_dir, f"{page_title_to_filename(title)}.txt")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(path, "w", encoding="utf-8") as f:
        f.write(wikitext)
    logging.info(f"Downloaded '{title}' to '{path}'")


def get_titles_from_csv(file: str = "data/download_combined.csv") -> list[str]:
    import pandas as pd
    df = pd.read_csv(file)
    return df['title'].tolist()

if __name__ == "__main__":
    titles_to_download = get_titles_from_csv()
    download_pages(titles_to_download)