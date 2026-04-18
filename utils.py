import os

def get_all_wiki_files(directory: str = "data/wiki_pages") -> list[str]:
    return [os.path.join(directory, f) for f in os.listdir(directory)]


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