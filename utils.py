import os

def get_all_wiki_files(directory: str = "data/wiki_pages") -> list[str]:
    return [os.path.join(directory, f) for f in os.listdir(directory)]
