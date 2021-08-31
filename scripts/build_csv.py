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
# TODO: make these optional parameters and print them out when --verbose
OWLNETS_SCRIPT: str = './owlnets_script/__main__.py'
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

# http://www.obofoundry.org/ontology/cl.html
# Elapsed time 0:00:21.838220
# Complete CL but with no imports or external axioms (Should be using this one but Jonathan's code breaks wih it at the moment)
CL_BASE_OWL_URL: str = 'http://purl.obolibrary.org/obo/cl/cl-base.owl'
# Elapsed time 0:02:55.045686
# Complete ontology, plus inter-ontology axioms, and imports modules
CL_OWL_URL: str = 'http://purl.obolibrary.org/obo/cl.owl'

# Elapsed time 17:23:51.998208
# http://www.obofoundry.org/ontology/chebi.html
CHEBI_OWL_URL: str = 'http://purl.obolibrary.org/obo/chebi.owl'

# BREAKS
# http://www.obofoundry.org/ontology/pr.html
PR_OWL_URL: str = 'http://purl.obolibrary.org/obo/pr.owl'

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

# OWL FILE IS NOT THERE 8/31/21
# http://www.ontobee.org/ontology/OGI
OGI_OWL_URL: str = 'http://purl.obolibrary.org/obo/ogi.owl'

# https://www.ebi.ac.uk/ols/ontologies/hsapdv
HSAPDV_OWL_URL: str = 'http://purl.obolibrary.org/obo/hsapdv.owl'

# BREAKS 8/30/21
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

# http://edamontology.org/page
EDAN_OWL_URL: str = 'http://edamontology.org/EDAM.owl'

# http://obofoundry.org/ontology/mp.html
MP_OWL_URL: str = 'http://purl.obolibrary.org/obo/mp.owl'

# OWL_URLS: list = [UBERON_OWL_URL, CL_OWL_URL, CHEBI_OWL_URL, PATO_OWL_URL, DOID_OWL_URL, OBI_OWL_URL, CCF_OWL_URL]
# More stuff....
OWL_URLS: list = [PATO_OWL_URL, UBERON_OWL_URL, CL_BASE_OWL_URL, DOID_OWL_URL, OBI_OWL_URL, CCF_OWL_URL, CHEBI_OWL_URL]
# OWL_URLS: list = [UBERON_OWL_URL, CL_BASE_OWL_URL, DOID_OWL_URL, OBI_OWL_URL, CCF_OWL_URL, CHEBI_OWL_URL]
# OWL_URLS: list = [UBERON_OWL_URL, CL_OWL_URL]

# TODO https://douroucouli.wordpress.com/2019/03/14/biological-knowledge-graph-modeling-design-patterns/


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(
    description='Build .csv files from .owl files using PheKnowLator and Jonathan''s script',
    formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument("-u", '--umls_csvs_dir', type=str, default='../neo4j/import/current',
                    help='the directory containing the UMLS Graph Extract .csv files modified by Jonathan''s script')
parser.add_argument("-l", "--owlnets_dir", type=str, default='./owlnets_output',
                    help='directory containing the owlnets directories from a run of PheKnowLator'
                         ' which is used by Jonathan''s script')
parser.add_argument("-t", "--owltools_dir", type=str, default='./pkt_kg/libs',
                    help='directory where the owltools executable is downloaded to')
parser.add_argument("-o", "--owl_dir", type=str, default='./owl',
                    help='directory used for the owl input files')
parser.add_argument("-O", "--oneOwl", type=str, default=None,
                    help='process only this one OWL file')
parser.add_argument("-c", "--clean", action="store_true",
                    help='clean the owlnets_output directory of previous output files before run')
parser.add_argument("-d", "--force_owl_download", action="store_true",
                    help='force downloading of the .owl file before processing')
parser.add_argument("-w", "--with_imports", action="store_true",
                    help='process OWL file even if imports are found, otherwise give up with an error')
parser.add_argument("-s", "--skipPheKnowLator", action="store_true",
                    help='assume that the PheKnowLator has been run and skip the run of it')
parser.add_argument("-S", "--skipValidation", action="store_true",
                    help='skip all validation')
parser.add_argument("-v", "--verbose", action="store_true",
                    help='increase output verbosity')

args = parser.parse_args()

log_dir, log, log_config = 'builds/logs', 'pkt_build_log.log', glob.glob('**/logging.ini', recursive=True)
logger = logging.getLogger(__name__)
logging.config.fileConfig(log_config[0], disable_existing_loggers=False, defaults={'log_file': log_dir + '/' + log})

# Both of these directories are found in the .gitignore file...
base_owlnets_dir = args.owlnets_dir
csvs_dir = args.umls_csvs_dir
owltools_dir = args.owltools_dir
owl_dir = args.owl_dir

if args.verbose is True:
    print('Parameters:')
    print(f" * Verbose mode")
    if args.clean is True:
        print(" * Cleaning owlnets directory")
    print(f" * Owlnets directory: {base_owlnets_dir} (exists: {os.path.isdir(base_owlnets_dir)})")
    print(f" * Owltools directory: {owltools_dir} (exists: {os.path.isdir(owltools_dir)})")
    print(f" * Owl directory: {owl_dir} (exists: {os.path.isdir(owl_dir)})")
    csvs_dir_islink = False
    if os.path.islink(csvs_dir) is True:
        csvs_dir_islink = os.path.realpath(csvs_dir)
    print(f" * Directory containing the UMLS Graph Extract .csv files to process: {csvs_dir} (exitst: {os.path.isdir(csvs_dir)}) (simlink: {csvs_dir_islink})")
    if args.force_owl_download is True:
        print(f" * PheKnowLator will force .owl file downloads")
    if args.with_imports is True:
        print(f" * PheKnowLator will run even if imports are found in .owl file")
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


def make_new_save_dir(path: str, save_dir: str) -> str:
    max_version: int = 0
    for filename in os.listdir(path):
        if re.match(f'^{save_dir}\.[0-9].*$', filename):
            current_version: int = int(filename.split('.', 1)[1])
            max_version = max(max_version, current_version)
    new_dir: str = f"{save_dir}.{max_version+1}"
    new_path: str = os.path.join(path, new_dir)
    os.mkdir(new_path)
    return new_path


def copy_csv_files_to_save_dir(path: str, save_dir: str) -> str:
    save_path: str = make_new_save_dir(path, save_dir)
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
            lines_fp: int = lines_in_file(fp)
            fp_save: str = os.path.join(save_path, filename)
            lines_fp_save: int = lines_in_file(fp_save)
            logger.info(f"Lines in files: {fp} {lines_fp}; {fp_save} {lines_fp_save}; difference: {lines_fp-lines_fp_save}")


for owl_url in OWL_URLS:
    processing_file: str = f"Processing OWL file: {owl_url}"
    print(processing_file)
    logger.info(processing_file)
    if args.skipPheKnowLator is not True:
        clean = ''
        if args.clean is True:
            clean = '--clean'
        force_owl_download = ''
        if args.force_owl_download is True:
            force_owl_download = '--force_owl_download'
        with_imports = ''
        if args.with_imports is True:
            with_imports = '--with_imports'
        owlnets_script: str = f"{OWLNETS_SCRIPT} {clean} {force_owl_download} {with_imports} -l {base_owlnets_dir} -t {owltools_dir} -o {owl_dir} {owl_url}"
        logger.info(f"Running: {owlnets_script}")
        os.system(owlnets_script)
    if args.skipValidation is not True:
        validation_script: str = f"{VALIDATION_SCRIPT} -o {csvs_dir} -l {base_owlnets_dir}"
        logger.info(f"Running: {validation_script}")
        os.system(validation_script)
    save_csv_dir = copy_csv_files_to_save_dir(csvs_dir, 'save')
    logger.info(f"Saving .csv files to directory: {save_csv_dir}")
    working_file: str = file_from_uri(owl_url)
    working_file_base: str = working_file.rsplit('.', 1)[0]
    working_owlnets_dir: str = base_owlnets_dir + os.path.sep + working_file_base
    owl_sab: str = working_file_base.upper()
    if owl_sab == 'CL-BASE':
        owl_sab = 'CL'
    umls_graph_script: str = f"{UMLS_GRAPH_SCRIPT} {working_owlnets_dir} {csvs_dir} {owl_sab}"
    logger.info(f"Running: {umls_graph_script}")
    os.system(umls_graph_script)
    lines_in_csv_files(csvs_dir, save_csv_dir)

# Add log entry for how long it took to do the processing...
elapsed_time = time.time() - start_time
logger.info('Done! Elapsed time %s', "{:0>8}".format(str(timedelta(seconds=elapsed_time))))
