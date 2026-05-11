import logging
import os
import datetime

from comnet.config import ERASE_PREVIOUS_LOGS

def setup_logging(name: str):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    if ERASE_PREVIOUS_LOGS:
        for file in os.listdir("logs"):
            if name not in file:
                continue
            file_path = os.path.join("logs", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    exact_date = datetime.datetime.now()
    path = f"logs/{name}_{exact_date.strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=path,
        filemode='w',
        encoding='utf-8'
    )

def setup_logging_download():
    setup_logging("wiki_download")

def setup_logging_parse():
    setup_logging("parser")
