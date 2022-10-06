#!/usr/bin/env python
# coding: utf-8

# Converts the CSV file downloaded (as a GZ archive) from BioPortal for the HuBMAP Samples Added Terms (HUSAT)
# ontology to OWLNETS format.

# This script is designed to align with the conversion logic executed in the build_csv.py script--e.g., outputs to
# owlnets_output, etc. This means: 1. The HUSAT CSV file will be extracted from GZ and downloaded to the OWL folder
# path, even though it is not an OWL file. 2. The OWLNETS output will be stored in the OWLNETS folder path.

# Because the HUSAT file will likely be small, the script will always download it. In addition,
# the script will not build a MD5 checksum.


import argparse
import gzip
import pandas as pd
import numpy as np
import os
import glob
import logging.config
import urllib
from urllib.request import Request


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(
    description='Convert the CSV file of the HUSAT (of which the URL is the required parameter) ontology to OWLNETs .\n'
                'In general you should not have the change any of the optional arguments',
    formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument('owl_url', type=str,
                    help='url for the CSV file to process')
parser.add_argument('owl_sab', type=str,
                    help='directory in --owlnets_dir and --owl_dir to save information from this run')
parser.add_argument("-l", "--owlnets_dir", type=str, default='./owlnets_output',
                    help='directory used for the owlnets output files')
parser.add_argument("-o", "--owl_dir", type=str, default='./owl',
                    help='directory used for the owl input files')
parser.add_argument("-v", "--verbose", action="store_true",
                    help='increase output verbosity')
args = parser.parse_args()

#owl_url ="https://data.bioontology.org/ontologies/HUSAT/download?apikey=4983e1fe-1f54-412e-99bb-74764d659cb0&download_format=csv"


# Use existing logging from build_csv.
# Note: To run this script directly as part of development or debugging
# (i.e., instead of calling it from build_csv.py), change the relative paths as follows:
# log_config = '../builds/logs'
# glob.glob('../**/logging.ini'...

log_dir, log, log_config = 'builds/logs', 'pkt_build_log.log', glob.glob('**/logging.ini', recursive=True)
logger = logging.getLogger(__name__)
logging.config.fileConfig(log_config[0], disable_existing_loggers=False, defaults={'log_file': log_dir + '/' + log})


def print_and_logger_info(message: str) -> None:
    print(message)
    logger.info(message)


if args.verbose is True:
    print('Parameters:')
    print(f" * Verbose mode")
    # if args.clean is True:
    # print(" * Cleaning owlnets directory")
    print(f" * CSV URL: {args.owl_url}")
    print(f" * CSV sab: {args.owl_sab}")
    print(f" * Owlnets directory: {args.owlnets_dir} (exists: {os.path.isdir(args.owlnets_dir)})")
    # print(f" * Owltools directory: {args.owltools_dir} (exists: {os.path.isdir(args.owltools_dir)})")
    print(f" * Owl directory: {args.owl_dir} (exists: {os.path.isdir(args.owl_dir)})")
    print('')

owl_dir: str = os.path.join(args.owl_dir, args.owl_sab)
os.system(f"mkdir -p {owl_dir}")

# Download HUSAT GZ from BioPortal.
request = Request(args.owl_url)
request.add_header('Accept-encoding', 'gzip')
response = urllib.request.urlopen(request)
zip_path = os.path.join(owl_dir, 'HUSAT.GZ')
with open(zip_path, 'wb') as fzip:
    while True:
        data = response.read()
        if len(data) == 0:
            break
        fzip.write(data)
print_and_logger_info("Downloaded HUSAT zip file.")

# Extract CSV file from Zip.
csv_path = os.path.join(owl_dir, 'HUSAT.CSV')
with gzip.open(zip_path, 'rt') as fzip:
    file_content = fzip.read()
with open(csv_path, 'w') as fout:
    fout.write(file_content)
print_and_logger_info("Extracted and stored HUSAT.CSV file.")

dfHUSAT = pd.read_csv(csv_path)

# Build OWLNETS text files.
# The OWLNETS format represents ontology data in a TSV in format:

# subject <tab> predicate <tab> object
#
# where:
#   subject - code for node in custom ontology
#   predicate - relationship
#   object: another code in the custom ontology

#  (In canonical OWLNETS, the relationship is a URI for a relation
#  property in a standard OBO ontology, such as RO.) For custom
#  ontologies such as HuBMAP, we use custom relationship strings.)

# For HUSAT, the only relationship is subClassOf.

owlnets_path: str = os.path.join(args.owlnets_dir, args.owl_sab)
os.system(f"mkdir -p {owlnets_path}")

edgelist_path: str = os.path.join(owlnets_path, 'OWLNETS_edgelist.txt')
print_and_logger_info('Building: ' + os.path.abspath(edgelist_path))

with open(edgelist_path, 'w') as out:
    out.write('subject' + '\t' + 'predicate' + '\t' + 'object' + '\n')
    for index, row in dfHUSAT.iterrows():

        if index >= 0:  # non-header
            subjIRI = str(row['Class ID'])
            subj = args.owl_sab + ' ' + subjIRI[subjIRI.rfind('/') + 1:len(subjIRI)]
            if str(row['Parents']) not in (np.nan, 'nan'):
                # Assumes 1 parent
                objIRI = str(row['Parents'])
                obj = args.owl_sab + ' ' + objIRI[objIRI.rfind('/') + 1:len(objIRI)]
                predicate = 'subClassOf'
                out.write(subj + '\t' + predicate + '\t' + obj + '\n')

# NODE METADATA
# Write a row for each unique concept in the 'code' column.

node_metadata_path: str = os.path.join(owlnets_path, 'OWLNETS_node_metadata.txt')
print_and_logger_info('Building: ' + os.path.abspath(node_metadata_path))

with open(node_metadata_path, 'w') as out:
    out.write(
        'node_id' + '\t' + 'node_namespace' + '\t' + 'node_label' + '\t' + 'node_definition' + '\t' + 'node_synonyms' + '\t' + 'node_dbxrefs' + '\n')
    # Root node
    #out.write(args.owl_sab + '_top' + '\t' + args.owl_sab + '\t' + 'top node' + '\t' + 'top node' + '\t' + '\t' '\n')
    for index, row in dfHUSAT.iterrows():
        if index >= 0:  # non-header
            nodeIRI = str(row['Class ID'])
            node_id = args.owl_sab + ' ' + nodeIRI[nodeIRI.rfind('/') + 1:len(nodeIRI)]
            node_namespace = args.owl_sab
            node_label = str(row['Preferred Label'])
            node_definition = str(row['Definitions'])
            node_synonyms = str(row['Synonyms'])

            # The synonym field is an optional pipe-delimited list of string values.
            if node_synonyms in (np.nan, 'nan'):
                node_synonyms = 'None'

            # Clear the dbxrefs column. The values from this column will be used to construct additional
            # subClassOf relationships.
            node_dbxrefs = 'None'
            out.write(
                node_id + '\t' + node_namespace + '\t' + node_label + '\t' + node_definition + '\t' + node_synonyms + '\t' + node_dbxrefs + '\n')

# RELATION METADATA
# Create a row for each type of relationship.

relation_path: str = os.path.join(owlnets_path, 'OWLNETS_relations.txt')
print_and_logger_info('Building: ' + os.path.abspath(relation_path))

with open(relation_path, 'w') as out:
    # header
    out.write(
        'relation_id' + '\t' + 'relation_namespace' + '\t' + 'relation_label' + '\t' + 'relation_definition' + '\n')
    # The only relationship is a subClassOf, which the OWLNETS-UMLS-GRAPH script will convert to an isa.
    out.write('subClassOf' + '\t' + args.owl_sab + '\t' + 'subClassOf' + '\t' + '' + '\n')
