import os
import time
import requests
import logging
from comnet.config import DOWNLOAD_INTERVAL_SEC, pipeline_type
from comnet.downloader.ww2.download_ww2 import get_ww2_battle_names
from comnet.shared.log_utils import setup_logging_download
from comnet.shared.utils import rawname_to_filename
from comnet.downloader.consts import DEFAULT_PARAMS, WIKI_API_URL, HEADERS, WW1_TITLES_CSV, WW2_TITLES_TXT, WIKI_PAGES_DIR

setup_logging_download()

def download_pages(titles: list[str], output_dir=WIKI_PAGES_DIR) -> None:
    for i, title in enumerate(titles):
        print(f"\rDownloading files... {i+1}/{len(titles)}", end="")
        
        if _is_saved(output_dir, title):
            logging.warning(f"Page '{title}' already downloaded. Skipping.")
            continue

        download_page(title, output_dir)
        time.sleep(DOWNLOAD_INTERVAL_SEC)
    print()

def _is_saved(output_dir: str, title: str) -> bool:
    path = os.path.join(output_dir, f"{rawname_to_filename(title)}")
    return os.path.exists(path)
    
def download_page(title: str, output_dir=WIKI_PAGES_DIR) -> None:
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
    
    _save_overwrite(output_dir, title, wikitext)

def _save_overwrite(output_dir: str, title: str, wikitext: str) -> None:
    path = os.path.join(output_dir, f"{rawname_to_filename(title)}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(path, "w", encoding="utf-8") as f:
        f.write(wikitext)
    logging.info(f"Downloaded '{title}' to '{path}'")


def get_ww1_titles(file: str = WW1_TITLES_CSV) -> list[str]:
    import pandas as pd
    df = pd.read_csv(file)
    return df['title'].tolist()

def get_ww2_titles(file: str = WW2_TITLES_TXT) -> list[str]:
    with open(file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def main():
    if pipeline_type == "ww1":
        titles_to_download = get_ww1_titles()
    elif pipeline_type == "ww2":
        titles_to_download = get_ww2_titles()
    else:
        raise ValueError(f"Unsupported pipeline type: {pipeline_type}")

    download_pages(titles_to_download)

if __name__ == "__main__":
    main()