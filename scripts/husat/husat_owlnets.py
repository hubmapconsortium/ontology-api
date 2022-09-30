#!/usr/bin/env python
# coding: utf-8

# Converts the CSV file downloaded from BioPortal for the HuBMAP Samples Added Terms (HUSAT) ontology to
# OWLNETS format.

# This script is designed to align with the PheKnowLator logic executed in the build_csv.py script--e.g., outputs
# to owlnets_output, etc.

import argparse
import sys
import pandas as pd
import numpy as np
import os
import glob
import logging.config
import subprocess
import hashlib

# Setup and running the script...
#
# $ cd scripts
# $ python3 -m venv venv
# $ source venv/bin/activate
# $ python --version
# Python 3.9.5
# $ pip install -r requirements.txt
# $ brew install wget

class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


parser = argparse.ArgumentParser(
    description='Builds ontology files in OWLNETS format from the HUSAT ontology.',
    formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument("-l", "--owlnets_dir", type=str, default="./owlnets_output",
                    help="directory containing the owlnets output directories")
args = parser.parse_args()

# Use existing logging from build_csv.
# Note: To run this script directly as part of development or debugging
# (i.e., instead of calling it from build_csv.py), change the relative paths as follows:
# log_config = '../builds/logs'
# glob.glob('../**/logging.ini'...

log_dir, log, log_config = '..builds/logs', 'pkt_build_log.log', glob.glob('../**/logging.ini', recursive=True)
logger = logging.getLogger(__name__)
logging.config.fileConfig(log_config[0], disable_existing_loggers=False, defaults={'log_file': log_dir + '/' + log})

def print_and_logger_info(message: str) -> None:
    print(message)
    logger.info(message)

def download_owl(url: str, loc: str, working_file: str, force_empty=True) -> str:
    logger.info(f'Downloading owl file from \'{url}\' to \'{loc}\'')

    cwd: str = os.getcwd()

    os.system(f"mkdir -p {loc}")
    os.chdir(loc)

    wgetResults: bytes = subprocess.check_output([f'wget {url}'], shell=True, stderr=subprocess.STDOUT)
    wgetResults_str: str = wgetResults.decode('utf-8')
    for line in wgetResults_str.strip().split('\n'):
        if 'Length: unspecified' in line:
            logger.error(f'Failed to download {uri}')
            print(f'Failed to download {uri}')
            print(wgetResults_str)
            exit(1)
    if args.verbose:
        print(wgetResults_str)

    md5: str = hashlib.md5(open(working_file, 'rb').read()).hexdigest()
    md5_file: str = f'{working_file}.md5'
    logger.info('MD5 for owl file {md5} saved to {md5_file}')
    with open(md5_file, 'w', newline='') as fp:
        fp.write(md5)

    os.chdir(cwd)


# Download HUSAT CSV file from BioPortal.
# Note: This script will alwoys download the file, and will not compare MD5.
working_dir: str = os.path.join(args.owlnets_dir, 'HUSAT')
logger.info("Make sure working directory '%s' exists", working_dir)
os.system(f"mkdir -p {working_dir}")

print_and_logger_info('Loading ontology')

if args.verbose:
    print_and_logger_info(f"Downloading .owl file to {owl_file} (force .owl download specified)")
download_owl(uri, owl_dir, working_file)