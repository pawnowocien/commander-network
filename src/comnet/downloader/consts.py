from comnet.config import USER_AGENT, pipeline_type

SKIP_INCLUDING = ["battleship", "Battleship", "Battlefield", "List_of", "order_of_battle", "(film)"]
EXTRACT_INCLUDING = ["battle", "Battle"]

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


WIKI_PAGES_DIR = f"data/{pipeline_type}/wiki_pages/"

WW1_TITLES_CSV = "data/ww1/_downloader_setup/download_combined.csv"
WW2_TITLES_TXT = "data/ww2/_downloader_setup/download_titles.txt"