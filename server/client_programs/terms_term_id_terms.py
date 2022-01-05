#!/usr/bin/env python

import argparse
from typing import Any, Dict, List, Optional, Union
import time, json, sys
sys.path.append('../hu-bmap-ontology-api-client')
from hu_bmap_ontology_api_client import Client
from hu_bmap_ontology_api_client.types import Response, Unset
from hu_bmap_ontology_api_client.api.default import terms_term_id_terms_get
from hu_bmap_ontology_api_client.models.term_resp_obj import TermRespObj


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(
    description='Run term_ids in input file through HuBMAP Ontoloty API and output one line for each to stdout',
    formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument('term_id_file',
                    help='file from which to read the term_id(s) to search')
parser.add_argument("-t", '--term_id', type=str,
                    help='process this one term_id and ignore the file if given')
parser.add_argument("-s", '--sep', type=str, default=',',
                    help='separator to use between to delineate attributes in object while printing')
parser.add_argument("-u", '--url', type=str, default='https://ontology-api.dev.hubmapconsortium.org',
                    help='base portion of the url to be used when accessing the HuBMAP Ontology API Server')
parser.add_argument("-v", "--verbose", action="store_true",
                    help='increase output verbosity writing to stderr')

args = parser.parse_args()

sep: str = args.sep


def eprint(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)


def print_term_resp_obj_header() -> None:
    print(f"code_id{sep}code_sab{sep}code{sep}concept{sep}tty{sep}term{sep}matched{sep}rel_type{sep}rel_sab")


def print_attribute(a, print_sep: bool) -> None:
    if print_sep is True:
        print(sep, end='')
    if type(a) is not Unset:
        print(a, end='')


def print_term_resp_obj(o: TermRespObj) -> None:
    print_attribute(o.code_id, False)
    print_attribute(o.code_sab, True)
    print_attribute(o.code, True)
    print_attribute(o.concept, True)
    print_attribute(o.tty, True)
    print_attribute(o.term, True)
    print_attribute(o.matched, True)
    print_attribute(o.rel_type, True)
    print_attribute(o.rel_sab, True)
    print('')


def print_data_for_term(term_id: str) -> None:
    start: int = time.time()
    response: Response[List[TermRespObj]] = terms_term_id_terms_get.sync_detailed(client=client, term_id=term_id)
    if args.verbose is True:
        end: int = time.time()
        eprint(f"Processing call to ontology API for term_id '{term_id}'; call time (sec): {end - start}")
    if response.status_code == 200:
        parsed: List[TermRespObj] = response.parsed
        parsed_len = len(parsed)
        if parsed_len > 0:
            if args.verbose is True:
                eprint(f"For term_id '{term_id}'; parsed_len: {parsed_len}")
            for termRespObj in parsed:
                print_term_resp_obj(termRespObj)
        else:
            eprint(f"No term response for term_id: {term_id}")
    else:
        eprint(f"Error reading from server; response.status_code = {response.status_code}")


def process_term_id_file(filename: str) -> None:
    start: int = time.time()
    with open(filename, "r") as file:
        lines = file.readlines()
        if args.verbose is True:
            eprint(f"Processing input file {filename}; lines in file: {len(lines)}")
        for line in lines:
            line = line.strip()
            print_data_for_term(line)
    end: int = time.time()
    if args.verbose is True:
        eprint(f"Processing time (sec): {end - start}")


# https://pypi.org/project/openapi-python-client/
client = Client(base_url=args.url)
# client = AuthenticatedClient(base_url=args.url, token="my-friend-bob")
timeout: int = 60
if args.verbose is True:
    eprint(f"Default client timeout (sec): {client.get_timeout()}")
    eprint(f"Setting client timeout to (sec): {timeout}")
client = client.with_timeout(timeout)

print_term_resp_obj_header()
if args.term_id is not None:
    print_data_for_term(args.term_id)
else:
    process_term_id_file(args.term_id_file)
