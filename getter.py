import requests
import click
from requests.exceptions import HTTPError
import utils


def get_dump(config):
    req = requests.get(
        "https://www.nationstates.net/pages/nations.xml.gz",
        headers={"User-Agent": utils.get_user_agent(config["nation"])},
        stream=True
    )

    try:
        req.raise_for_status()
    except HTTPError:
        click.echo("[ERROR] Could not download dump")
        return False

    with open("nations.xml.gz", 'wb') as dumpfile:
        for chunk in req.iter_content(chunk_size=1024 * 1024):
            dumpfile.write(chunk)

    click.echo("[INFO] Dump downloaded and written")
    return True
