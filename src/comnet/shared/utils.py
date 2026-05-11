import os

from comnet.shared.consts import STATIC_FILES_TO_SKIP

def page_title_to_filename(title: str) -> str:
    return title.replace("/", "__")

def raw_name_to_link(name: str) -> str:
    return f"https://en.wikipedia.org/wiki/{name}"

def get_all_wiki_files(directory: str = "data/wiki_pages") -> list[str]:
    return [os.path.join(directory, f) for f in os.listdir(directory)]

def get_filtered_wiki_files(directory: str = "data/wiki_pages") -> list[str]:
    all_files = get_all_wiki_files(directory)
    files_to_skip = get_files_to_skip()
    return [f for f in all_files if os.path.basename(f) not in files_to_skip]

def get_files_to_skip() -> list[str]:
    return STATIC_FILES_TO_SKIP + get_redirects()

def get_redirects(directory: str = "data/wiki_pages") -> list[str]:
    redirects = []
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
            content = f.read()
            if "#REDIRECT" in content or "#redirect" in content:
                redirects.append(file)
    return redirects

if __name__ == "__main__":
    print(get_redirects())