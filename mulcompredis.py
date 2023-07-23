"""
This performs the same job as the single.py but it uses Redis
as a form of other computers listening to the queue for jobs
"""
import logging
import os

from dotenv import load_dotenv
from redis import Redis
from rq import Queue

from download import download_link, get_links, setup_download_dir

# from downloadcompredis import get_links, download_link

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


def main():
    # load the .env file
    load_dotenv()
    client_id = os.getenv("IMGUR_CLIENT_ID")
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable")
    download_dir = setup_download_dir()
    links = get_links(client_id=client_id)
    q = Queue(connection=Redis(host="localhost", port=6379))

    for link in links:
        q.enqueue(download_link, download_dir, link)


if __name__ == "__main__":
    main()
