import json
import logging
import os
from pathlib import Path
from urllib.request import Request, urlopen

# declare the logger
logger = logging.getLogger(__name__)

# declare the types
types = {
    "image/jpeg",
    "image/png",
}


def get_links(client_id):
    headers = {
        "Authorization": "Client-ID {}".format(client_id),
    }

    req = Request(
        url="https://api.imgur.com/3/gallery/random/random/",
        headers=headers,
        method="GET",
    )

    with urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return [item["link"] for item in data["data"] if "type" in item and item["type"] in types]


def download_link(directory, link):
    download_path = directory / os.path.basename(link)
    with urlopen(link) as image, download_path.open("wb") as f:
        f.write(image.read())
        logger.info("Downloaded %s", link)


def setup_download_dir():
    download_dir = Path("images")
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir
