import logging
import os
import datetime

def setup_logging(name: str):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    exact_date = datetime.datetime.now()
    path = f"logs/{name}_{exact_date.strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=path,
        filemode='w'
    )

def setup_logging_download():
    setup_logging("wiki_download")

def setup_logging_parse():
    setup_logging("parser")
