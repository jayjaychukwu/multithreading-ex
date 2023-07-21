import logging
import os
from time import time

from dotenv import load_dotenv

from download import download_link, get_links, setup_download_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main():
    ts = time()
    # load the .env file
    load_dotenv()
    client_id = os.getenv("IMGUR_CLIENT_ID")
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable")
    download_dir = setup_download_dir()
    links = get_links(client_id=client_id)
    for link in links:
        download_link(directory=download_dir, link=link)

    logging.info("Took %s seconds", time() - ts)


if __name__ == "__main__":
    main()
