import pandas as pd
from consts import SKIP_INCLUDING, EXTRACT_INCLUDING

def create_diff_csv(larger_file: str = "data/download_all.csv", 
                    smaller_file: str = "data/download_filter.csv", 
                    output_file: str = "data/download_diff.csv",
                    skip_including: list[str] = SKIP_INCLUDING,
                    extract_including: list[str] = EXTRACT_INCLUDING):
    larger_file = pd.read_csv(larger_file)
    smaller_file = pd.read_csv(smaller_file)

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
    diff_df.to_csv(output_file, index=False)

def print_titles_and_links(file: str = "data/download_diff.csv", just_links: bool = False):
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

def combine_files(file1: str = "data/download_filter.csv", 
                  file2: str = "data/download_diff.csv", 
                  output_file: str = "data/download_combined.csv"):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    combined_df = pd.concat([df1, df2], ignore_index=True)
    combined_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    create_diff_csv()
    combine_files()
    # print_titles_and_links(just_links=True)