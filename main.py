import gzip
import click
import psycopg
import requests
from lxml import etree
import tomllib
from requests.exceptions import HTTPError

version = "0.1.0"


def get_user_agent(nation: str):
    user_agent = f"GreenDumper {version} "
    f"/ Developed by nation:TheSapphire "
    f"/ Operated by nation:{nation}"
    return user_agent


def get_dump():
    config = get_config()

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

    click.echo("[INFO] Dump downloaded and written")
    return True


def fast_iter(context, func, *args, **kwargs):
    """
    http://lxml.de/parsing.html#modifying-the-tree
    Based on Liza Daly's fast_iter
    http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    See also http://effbot.org/zone/element-iterparse.htm
    """
    for event, elem in context:
        func(elem, *args, **kwargs)
        # It's safe to call clear() here because no descendants will be
        # accessed
        elem.clear()
        # Also eliminate now-empty references from the root node to elem
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context


def process_nation(elem, config):
    name = elem.find("NAME").text.lower().replace(" ", "_")
    dbid = elem.find("DBID").text
    region = elem.find("REGION").text.lower().replace(" ", "_")
    unstatus = elem.find("UNSTATUS").text


def get_config():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    return config


def process_dump():
    config = get_config()
    context = etree.iterparse(gzip.GzipFile("nations.xml.gz"), tag="NATION")
    fast_iter(context, process_nation, config)


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
