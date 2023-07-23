"""
Utilizing httpx to better support
multiprocesses
"""
import logging
import os

import httpx

from download import logger, types


def get_links(client_id):
    headers = {
        "Authorization": "Client-ID {}".format(client_id),
    }

    with httpx.Client() as client:
        response = client.get(
            "https://api.imgur.com/3/gallery/random/random/",
            headers=headers,
        )
        data = response.json()

    return [item["link"] for item in data["data"] if "type" in item and item["type"] in types]


def download_link(directory, link):
    download_path = directory / os.path.basename(link)
    with httpx.stream("GET", link) as response:
        with download_path.open("wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
    logger.info("Downloaded %s", link)
