import logging
import os
from queue import Queue
from threading import Thread
from time import time

from dotenv import load_dotenv

from download import download_link, get_links, setup_download_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            try:
                download_link(directory=directory, link=link)
            finally:
                self.queue.task_done()


def main():
    ts = time()
    load_dotenv()
    client_id = os.getenv("IMGUR_CLIENT_ID")
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable")

    download_dir = setup_download_dir()
    links = get_links(client_id=client_id)

    # create a queue to communicate with the worker threads
    queue = Queue()

    # create 8 worker threads
    for x in range(8):
        worker = DownloadWorker(queue=queue)

    # setting daemon to True will let the main thread exit even though the workers are blocking
    worker.daemon = True
    worker.start()

    # put the tasks into the queue as a tuple
    for link in links:
        logger.info("Queueing {}".format(link))
        queue.put((download_dir, link))

    # causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logging.info("Took %s", time() - ts)


if __name__ == "__main__":
    main()
