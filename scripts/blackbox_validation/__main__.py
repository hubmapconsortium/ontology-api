#!/usr/bin/env python

import argparse
from rdflib import *
import glob
import logging.config
import time
from datetime import timedelta
import urllib.request
from lxml import etree


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(description='Blackbox test newly generated .csv files.\n'
                                             'In general you should not have the change any of the optional arguments',
                                 formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument('owl_url', type=str, help='url for the OWL file used in the process')
parser.add_argument("-o", "--csv_original", action="store_true", default='../neo4j/import',
                    help='directory containing the original .csv files')
parser.add_argument("-n", "--csv_new", action="store_true", default='./csv_output',
                    help='directory containing the newly created .csv files')
parser.add_argument("-l", "--owlnets", action="store_true", default='./owlnets_output',
                    help='directory containing the owlnets files')
args = parser.parse_args()

csv_original_dir = args.csv_original
csv_new_dir = args.csv_new
owlnets_dir = args.owlnets
uri = args.owl_url

log_dir, log, log_config = 'builds/logs', 'pkt_build_log.log', glob.glob('**/logging.ini', recursive=True)
logger = logging.getLogger(__name__)
logging.config.fileConfig(log_config[0], disable_existing_loggers=False, defaults={'log_file': log_dir + '/' + log})


def scan_owl_xml_for_imports(url: str) -> list:
    # opener: urllib.OpenerDirector = urllib.request.build_opener()
    # tree: etree.ElementTree = etree.parse(opener.open(url))
    tree: etree.ElementTree = etree.parse(url)
    # https://docs.python.org/3/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
    imports: list = tree.findall('owl:Ontology/owl:imports', namespaces={'owl': 'http://www.w3.org/2002/07/owl#'})
    resources: list = []
    for i in imports:
        resource: str = i.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'+'resource')
        resources.append(resource)
    return resources


start_time = time.time()

logger.info(f"Processing '{uri}'")

# Read the xml aid determine if it contains any imports
graph = Graph().parse(uri, format='xml')
imports: list = scan_owl_xml_for_imports(uri)
if len(imports) != 0:
    logger.info(f"Found the following imports: {', '.join(imports)}")
else:
    logger.info("No imports were found")


# Add log entry for how long it took to do the processing...
elapsed_time = time.time() - start_time
logger.info('Done! Elapsed time %s', "{:0>8}".format(str(timedelta(seconds=elapsed_time))))
