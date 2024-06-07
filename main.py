import click
# import psycopg
import requests
import tomllib
from requests.exceptions import HTTPError

version = "0.1.0"


def get_user_agent(nation: str):
    user_agent = f"GreenDumper {version} "
    f"/ Developed by nation:TheSapphire "
    f"/ Operated by nation:{nation}"
    return user_agent


def get_dump():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    req = requests.get(
        "https://www.nationstates.net/pages/nations.xml.gz",
        headers={"User-Agent": get_user_agent(config["nation"])},
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

    click.echo("[INFO] Dump written")
    return True


def process_dump():
    pass


@click.group()
def cli():
    pass


@cli.command(help="Downloads NS nations dump")
def download():
    get_dump()


@cli.command(help="Processes a downloaded dump")
def process():
    process_dump()


@cli.command(help="Download and process dump")
def update():
    if get_dump():
        process_dump()


if __name__ == '__main__':
    cli()
