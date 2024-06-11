from lxml import etree
from gzip import GzipFile
import psycopg
import json


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


def process_nation(elem, cursor):
    nation = elem.find("NAME").text.lower().replace(" ", "_")
    region = elem.find("REGION").text.lower().replace(" ", "_")
    dbid = elem.find("DBID").text
    unstatus = elem.find("UNSTATUS").text
    endo = (
        []
        if elem.find("ENDORSEMENTS").text is None
        else elem.find("ENDORSEMENTS").text.split(",")
    )
    endojson = json.dumps(endo)
    cursor.execute(
        "INSERT INTO nsdump (nsid, nation, region, unstatus, endos) VALUES (%s, %s, %s, %s, %s)",
        (dbid, nation, region, unstatus, endojson)
    )


def process_dump(config):
    with psycopg.connect(config["dsn"]) as session:
        with session.cursor() as cursor:
            cursor.execute("TRUNCATE nsdump;")
            context = etree.iterparse(GzipFile("nations.xml.gz"), tag='NATION', events=('end',))
            fast_iter(context, process_nation, cursor)
            session.commit()
