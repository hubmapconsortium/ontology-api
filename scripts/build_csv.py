#!/usr/bin/env python

import argparse
import os
import shutil
import glob
import logging.config
import time
import re
import subprocess
from datetime import timedelta

OWLNETS_SCRIPT: str = './owlnets_script/__main__.py -c '
VALIDATION_SCRIPT: str = './blackbox_validation/__main__.py'
UMLS_GRAPH_SCRIPT: str = './Jonathan/OWLNETS-UMLS-GRAPH.py'

# All 'Elapsed time' on a Mac Book Pro (32Gb, 2.6 GHz 6-Core Intel Core i7)

# Elapsed time 0:08:03.189532
# https://uberon.github.io/downloads.html
# This one contain data without references....
UBERON_OWL_URL: str = 'http://purl.obolibrary.org/obo/uberon.owl'
# This one needs processing (see https://robot.obolibrary.org/merge ) to include references...
# UBERON_EXT_OWL_URL: str = 'http://purl.obolibrary.org/obo/uberon/ext.owl'

# This should get relationships and inverses and the RO code where we want the name...
# http://www.obofoundry.org/ontology/ro.html
# RO_URL: str = 'http://purl.obolibrary.org/obo/ro.owl'

# Elapsed time 0:02:55.045686
# http://www.obofoundry.org/ontology/cl.html
# Complete ontology, plus inter-ontology axioms, and imports modules
CL_OWL_URL: str = 'http://purl.obolibrary.org/obo/cl.owl'

# Elapsed time 17:23:51.998208
# http://www.obofoundry.org/ontology/chebi.html
CHEBL_OWL_URL: str = 'http://purl.obolibrary.org/obo/chebi.owl'

# BREAKS
# http://www.obofoundry.org/ontology/pr.html
PRO_OWL_URL: str = 'http://purl.obolibrary.org/obo/pr.owl'

# Elapsed time 0:00:38.827207
# http://www.obofoundry.org/ontology/pato.html
PATO_OWL_URL: str = 'http://purl.obolibrary.org/obo/pato.owl'

# Elapsed time 0:02:44.425941
DOID_OWL_URL: str = 'http://purl.obolibrary.org/obo/doid.owl'

# Elapsed time 0:00:14.051567
OBI_OWL_URL: str = 'http://purl.obolibrary.org/obo/obi.owl'

# Elapsed time 0:00:09.053144
# Note: currently has just AS (using ccf_part_of as the relationship), but could be a start.
CCF_OWL_URL: str = 'https://ccf-ontology.hubmapconsortium.org/ccf.owl'

# http://www.ontobee.org/ontology/OGI
OGI_OWL_URL: str = 'http://purl.obolibrary.org/obo/ogi.owl'

# https://www.ebi.ac.uk/ols/ontologies/hsapdv
HSAPVD_OWL_URL: str = 'http://purl.obolibrary.org/obo/hsapdv.owl'

# https://www.ebi.ac.uk/ols/ontologies/vario
VARIO_OWL_URL: str = 'http://purl.obolibrary.org/obo/vario.owl'

# https://bioportal.bioontology.org/ontologies/ORDO
ORDO_OWL_URL: str = 'https://data.bioontology.org/ontologies/ORDO/submissions/22/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb'

# http://brg.ai.sri.com/CCO/
CCO_OWL_URL: str = 'http://brg.ai.sri.com/CCO/downloads/cco.owl'

# https://www.ebi.ac.uk/ols/ontologies/mi
MI_OWL_URL: str = 'http://purl.obolibrary.org/obo/mi.owl'

# https://www.ebi.ac.uk/sbo/main/
SBO_OWL_URL: str = 'http://www.ebi.ac.uk/sbo/exports/Main/SBO_OWL.owl'

# OWL_URLS: list = [UBERON_OWL_URL, CL_OWL_URL, CHEBL_OWL_URL, PATO_OWL_URL, DOID_OWL_URL, OBI_OWL_URL, CCF_OWL_URL]
# More stuff....
# OWL_URLS: list = [UBERON_OWL_URL, CL_OWL_URL, DOID_OWL_URL, OBI_OWL_URL, CCF_OWL_URL, CHEBL_OWL_URL]
OWL_URLS: list = [UBERON_OWL_URL, CL_OWL_URL]


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(description='Build .csv files from .owl files using PheKnowLator and Jonathan''s script',
                                 formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--clean", action="store_true",
                    help='clean the owlnets_output directory of previous output files before run')
parser.add_argument("-l", "--owlnets", action="store_true", default='./owlnets_output',
                    help='directory containing the owlnets directories from a run of PheKnowLator'
                         ' which is used by Jonathan''s script')
parser.add_argument("-t", "--owltools", type=str, default='./pkt_kg/libs',
                    help='directory where the owltools executable is downloaded to')
parser.add_argument("-C", "--csvs", type=str, default='../neo4j/import',
                    help='directory where the .csv files modified by Jonathan''s script are located')
parser.add_argument("-s", "--skipPheKnowLator", action="store_true",
                    help='assume that the PheKnowLator has been run and skip the run of it')
parser.add_argument("-o", "--oneOwl", type=str, default=None,
                    help='process only this one OWL file')
parser.add_argument("-S", "--skipValidation", action="store_true",
                    help='skip all validation')
parser.add_argument("-v", "--verbose", action="store_true",
                    help='increase output verbosity')

args = parser.parse_args()

log_dir, log, log_config = 'builds/logs', 'pkt_build_log.log', glob.glob('**/logging.ini', recursive=True)
logger = logging.getLogger(__name__)
logging.config.fileConfig(log_config[0], disable_existing_loggers=False, defaults={'log_file': log_dir + '/' + log})

# Both of these directories are found in the .gitignore file...
base_owlnets_dir = args.owlnets
csvs_dir = args.csvs
owltools_dir = args.owltools

if args.verbose is True:
    print('Parameters:')
    if args.clean is True:
        print(" * Cleaning owlnets directory")
    print(f" * Owlnets directory: {base_owlnets_dir}")
    print(f" * Owltools directory: {owltools_dir}")
    print(f" * Csvs directory: {csvs_dir}")
    if args.skipPheKnowLator is True:
         print(f" * Skip PheKnowLator run")
    if args.oneOwl is not None:
        print(f" * Process only one OWL file: {args.oneOwl}")
    if args.skipValidation is True:
        print(' * Skipping all validation')
    print('')

if args.oneOwl is not None:
    OWL_URLS: list = [ args.oneOwl ]

logger.info(f"Processing OWL files: {', '.join(OWL_URLS)}")
start_time = time.time()


def file_from_uri(uri_str: str) -> str:
    if uri_str.find('/'):
        return uri_str.rsplit('/', 1)[1]


def new_save_dir(path: str, save_dir: str) -> str:
    save_dirs = []
    for filename in os.listdir(path):
        if re.match(f'^{save_dir}\.[0-9].*$', filename):
            save_dirs.append(filename)
    new_dir = f"{save_dir}.{len(save_dirs)+1}"
    new_path: str = os.path.join(path, new_dir)
    os.mkdir(new_path)
    return new_path


def copy_csv_files_to_save_dir(path: str, save_dir: str) -> str:
    save_path: str = new_save_dir(path, save_dir)
    for filename in os.listdir(path):
        if re.match(f'^.*\.csv$', filename):
            fp_src: str = os.path.join(path, filename)
            fp_dst: str = os.path.join(save_path, filename)
            shutil.copyfile(fp_src, fp_dst)
    logger.info(f"Copied {len(os.listdir(save_path))} files from {path} to {save_path}")
    return save_path


def lines_in_file(path: str) -> int:
    return int(subprocess.check_output(f"/usr/bin/wc -l {path}", shell=True).split()[0])


def lines_in_csv_files(path: str, save_path: str) -> None:
    for filename in os.listdir(path):
        if re.match(f'^.*\.csv$', filename):
            fp: str = os.path.join(path, filename)
            lines_fp = lines_in_file(fp)
            fp_save: str = os.path.join(save_path, filename)
            lines_fp_save = lines_in_file(fp_save)
            logger.info(f"Lines in files: {fp} {lines_fp}; {fp_save} {lines_fp_save}; difference: {lines_fp-lines_fp_save}")


for owl_url in OWL_URLS:
    print(f"Processing OWL file: {owl_url}")
    if args.skipPheKnowLator is not True:
        print(f"Running: {OWLNETS_SCRIPT} -c {args.clean} -l {base_owlnets_dir} -t {owltools_dir} {owl_url}")
        os.system(f"{OWLNETS_SCRIPT} -c {args.clean} -l {base_owlnets_dir} -t {owltools_dir} {owl_url}")
    if args.skipValidation is not True:
        print(f"Running: {VALIDATION_SCRIPT} -o {csvs_dir} -l {base_owlnets_dir}")
        os.system(f"{VALIDATION_SCRIPT} -o {csvs_dir} -l {base_owlnets_dir}")
    save_csv_dir = copy_csv_files_to_save_dir(csvs_dir, 'save')
    logger.info(f"Saving .csv files to directory: {save_csv_dir}")
    working_file: str = file_from_uri(owl_url)
    working_owlnets_dir: str = base_owlnets_dir + os.path.sep + working_file.rsplit('.', 1)[0]
    os.system(f"{UMLS_GRAPH_SCRIPT} {working_owlnets_dir} {csvs_dir}")
    # Here’s some specific guidance - the following should have numbers and the rest zero:
    # CODEs, SUIs, CUIs, CUI-CUIs, CUI-CODEs, CUI-SUIs, CODE-SUIs
    lines_in_csv_files(csvs_dir, save_csv_dir)


# Add log entry for how long it took to do the processing...
elapsed_time = time.time() - start_time
logger.info('Done! Elapsed time %s', "{:0>8}".format(str(timedelta(seconds=elapsed_time))))
