import pandas as pd
from comnet.downloader.consts import SKIP_INCLUDING, EXTRACT_INCLUDING

DIR_PATH = "data/ww1/_downloader_setup/"

ALL_PATH = DIR_PATH + "download_all.csv"
FIL_PATH = DIR_PATH + "download_filtered.csv"
DIF_PATH = DIR_PATH + "download_diff.csv"


def create_diff_csv(larger_filename: str = ALL_PATH, 
                    smaller_filename: str = FIL_PATH, 
                    output_filename: str = DIF_PATH,
                    skip_including: list[str] = SKIP_INCLUDING,
                    extract_including: list[str] = EXTRACT_INCLUDING):
    larger_file = pd.read_csv(larger_filename)
    smaller_file = pd.read_csv(smaller_filename)

    ids_larger = set(larger_file['pageid'])
    ids_smaller = set(smaller_file['pageid'])
    ids_only_larger = ids_larger - ids_smaller

    len_before = len(ids_only_larger)
    diff_df = larger_file[larger_file['pageid'].isin(ids_only_larger)]

    for word in skip_including:
        diff_df = diff_df[~diff_df['title'].str.contains(word, case=False, regex=False)]

    for word in extract_including:
        diff_df = diff_df[diff_df['title'].str.contains(word, case=False, regex=False)]

    len_dropped = len_before - len(diff_df)
    print(f"Dropped {len_dropped} rows")
    diff_df.to_csv(output_filename, index=False)

def print_titles_and_links(file: str = DIF_PATH, just_links: bool = False):
    def make_link(title: str) -> str:
        base_url = "https://en.wikipedia.org/wiki/"
        return base_url + title
    df = pd.read_csv(file)
    for i, title in enumerate(sorted(df['title']), start=1):
        if just_links:
            print(make_link(title))
        else:
            print(f"{i}. {title}")
            print(f"   {make_link(title)}")

def combine_files(file1: str = FIL_PATH, 
                  file2: str = DIF_PATH, 
                  output_file: str = DIR_PATH + "download_combined.csv"):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    combined_df = pd.concat([df1, df2], ignore_index=True)
    combined_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    create_diff_csv()
    combine_files()