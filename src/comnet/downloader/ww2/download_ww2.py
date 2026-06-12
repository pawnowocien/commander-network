import mwparserfromhell as mwp
import requests
import csv
import time  # <-- Added time module for the delay
import os    # <-- Added os to ensure directories exist
from comnet.downloader.consts import WIKI_API_URL, HEADERS, DEFAULT_PARAMS

TXT_PATH = "data/ww2/_downloader_setup/download_titles.txt"


def get_ww2_battle_names():
    params = {
        **DEFAULT_PARAMS,
        "titles": "List_of_World_War_II_battles"
    }
    
    print("Fetching battle list from Wikipedia...")
    response = requests.get(WIKI_API_URL, params=params, headers=HEADERS)
    data = response.json()

    # Safely get the first page whether the API returns a list or a dict
    pages_data = data['query']['pages']
    page = pages_data[0] if isinstance(pages_data, list) else list(pages_data.values())[0]
    
    if "missing" in page:
        print("Error: Page not found.")
        return
    
    wikitext = page['revisions'][0]['slots']['main']['content']
    parsed = mwp.parse(wikitext)
    
    battle_names = []

    for row in parsed.filter_tags(matches=lambda tag: str(tag.tag).lower() == 'tr'):
        cells = [tag for tag in row.contents.filter_tags(recursive=False) 
                 if str(tag.tag).lower() == 'td']
        
        # FIXED: Changed from `len(cells) < 3` to `not cells` to catch rowspan battles!
        if not cells:
            continue 
            
        first_cell = cells[0]
        
        if first_cell.contents:
            links = first_cell.contents.filter_wikilinks()
            if links:
                # Grab the title, strip whitespace, and swap spaces for underscores
                page_title = str(links[0].title).strip().replace(' ', '_')
                battle_names.append(page_title)

    # Ensure the directory exists before writing
    os.makedirs(os.path.dirname(TXT_PATH), exist_ok=True)

    # Print out just the pure link names to text file
    print(f"Saving {len(battle_names)} battle names to {TXT_PATH}...")
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        for name in battle_names:
            f.write(name + "\n")


# def download_all_ww2_battle_pages():
#     with open(TXT_PATH, "r", encoding="utf-8") as f:
#         # Ignore empty lines just in case
#         battle_names = [line.strip() for line in f.readlines() if line.strip()]
    
#     # Ensure the download directory exists
#     os.makedirs("data/ww2/wiki_pages", exist_ok=True)
    
#     for i, name in enumerate(battle_names):
#         if os.path.exists(os.path.join("data/ww2/wiki_pages", f"{name}.txt")):
#             continue

#         while True:
#             try:
#                 print(f"Downloading page {i+1}/{len(battle_names)}: {name}")
#                 download_page(name, output_dir="data/ww2/wiki_pages")
#                 break  # Break out of the retry loop if successful
#             except Exception as e:
#                 print(f"Error downloading '{name}': {e}. Retrying in 10 seconds...")
#                 time.sleep(10)  # Wait before retrying
        
#         time.sleep(5)

if __name__ == "__main__":
    get_ww2_battle_names()
    # download_all_ww2_battle_pages()