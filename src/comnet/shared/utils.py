import os

from comnet.shared.consts import STATIC_BATTLES_TO_SKIP

def rawname_to_safename(title: str) -> str:
    return title.replace("/", "__").replace(",", "--")
def safename_to_rawname(safename: str) -> str:
    return safename.replace("__", "/").replace("--", ",")

def rawname_to_filename(title: str) -> str:
    return rawname_to_safename(title) + ".txt"
def filename_to_rawname(filename: str) -> str:
    return safename_to_rawname(filename.replace(".txt", ""))

def rawname_to_link(name: str) -> str:
    return f"https://en.wikipedia.org/wiki/{name}"

def filepath_to_rawname(filepath: str) -> str:
    return filename_to_rawname(os.path.basename(filepath))

def get_all_wiki_files(directory: str = "data/wiki_pages") -> list[str]:
    return [os.path.join(directory, f) for f in os.listdir(directory)]

def get_filtered_wiki_files(directory: str = "data/wiki_pages") -> list[str]:
    all_files = get_all_wiki_files(directory)
    files_to_skip = get_files_to_skip()
    return [f for f in all_files if os.path.basename(f) not in files_to_skip]

def get_files_to_skip() -> list[str]:
    filenames = [rawname_to_filename(f) for f in STATIC_BATTLES_TO_SKIP]
    return filenames + get_redirects()

def get_redirects(directory: str = "data/wiki_pages") -> list[str]:
    redirects = []
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
            content = f.read()
            if "#REDIRECT" in content or "#redirect" in content:
                redirects.append(file)
    return redirects