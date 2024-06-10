from lxml import etree
from gzip import GzipFile
import psycopg


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


def process_nation(elem, session):
    nation = {}
    nation["name"] = elem.find("NAME").text.lower().replace(" ", "_")
    nation["region"] = elem.find("REGION").text.lower().replace(" ", "_")
    nation["dbid"] = elem.find("DBID").text
    nation["unstatus"] = elem.find("UNSTATUS").text
    nation["endo"] = (
        0
        if elem.find("ENDORSEMENTS").text is None
        else elem.find("ENDORSEMENTS").text
    )
    print(nation)


def process_dump(config):
    session = None
    context = etree.iterparse(GzipFile("nations.xml.gz"), tag='NATION', events=('end',))
    fast_iter(context, process_nation, session)
