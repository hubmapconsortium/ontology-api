#!/usr/bin/env python
# coding: utf-8

# # SimpleKnowledge to OWLNETS converter
# 
# Uses the input spreadsheet for the SimpleKnowledge Editor to generate a set of text files that comply with the
# OWLNETS format, as described in https://github.com/callahantiff/PheKnowLator/blob/master/notebooks
# /OWLNETS_Example_Application.ipynb.
# 
# User guide to build the SimpleKnowledge Editor spreadsheet:
# https://docs.google.com/document/d/1wjsOzJYRV2FRehX7NQI74ZKRXvH45l0QmClBBF_VypM/edit?usp=sharing

# SimpleKnowledge to OWLNETS converter

# Uses the input spreadsheet for the SimpleKnowledge Editor to generate text files that comply with the OWLNETS format.

import argparse
import sys
import pandas as pd
import numpy as np
import os


# Parse an argument that identifies the version of the UMLS in Neptune from which to build
# the CSV files.
class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


parser = argparse.ArgumentParser(
    description='Builds ontology files in OWLNETS format from a spreadsheet in SimpleKnowledge format.',
    formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument("skfile", help="SimpleKnowledge spreadsheet name")
parser.add_argument("ontology", help="Name of ontology")
args = parser.parse_args()

# Read input spreadsheet.
try:
    df_sk = pd.read_excel(args.skfile, sheet_name='SimpleKnowledgeEditor')
except FileNotFoundError:
    err = 'Missing input spreadsheet: ' + args.skfile
    raise SystemExit(err)

# Build OWLNETS text files.
# The OWLNETS format represents ontology data in a TSV in format:

# subject <tab> predicate <tab> object
#
# where:
#   subject - code for node in custom ontology
#   predicate - relationship
#   object: another code in the custom ontology
#
#  (In canonical OWLNETS, the relationship is a URI for a relation 
#  property in a standard OBO ontology, such as RO.) For custom
#  ontologies such as HuBMAP, we use custom relationship strings.)

edge_list_filename = './OWLNETS_edgelist.txt'
print('Building OWLNETS_edge')
with open(edge_list_filename, 'w') as out:
    out.write('subject' + '\t' + 'predicate' + '\t' + 'object' + '\n')

    # Each column after E in the spreadsheet (isa, etc.) represents a type of
    # subject-predicate_object relationship.
    #   1. Column F represents the isa relationship. 
    #   2. Columns after F represent relationships other than isa.

    # Cells in relationship columns contain comma-separated lists of object nodes.

    # Thus, a relationship cell, in general, represents a set of subject-predicate-object
    # relationships between the concept in the "code" cell and the concepts in the relationship
    # cell.

    for index, row in df_sk.iterrows():

        if index > 0:  # non-header
            subject = str(row['code'])

            for col in range(5, len(row)):
                # Obtain relationship.
                if col == 5:
                    predicate_uri = 'isa'
                else:
                    colhead = df_sk.columns[col]
                    # predicate_uri = colhead[colhead.find('(')+1:colhead.find(')')]
                    predicate_uri = colhead

                # Obtain codes in the proposed ontology for object concepts involved
                # in subject-predicate-object relationships.
                objects = row.iloc[col]

                if not pd.isna(objects):

                    listobjects = objects.split(',')

                    for obj in listobjects:
                        # Match object terms with their respective codes (Column A),
                        # which will result in a dataframe of one row.
                        match = df_sk[df_sk['term'] == obj]
                        if match.size == 0:
                            err = 'Error: row for \'' + subject + '\' indicates relationship \'' + predicate_uri
                            err = err + '\' with node \'' + obj + '\', but this node is not defined in the \'term\' '
                            err = err + 'column. (Check for spelling and case of node name.)'
                            raise SystemExit(err)

                        objcode = match.iloc[0, 1]
                        out.write(subject + '\t' + predicate_uri + '\t' + str(objcode) + '\n')

# NODE METADATA
# Write a row for each unique concept in in the 'code' column.

node_metadata_filename = './OWLNETS_node_metadata.txt'
print('Building OWLNETS_node_metadata')
with open(node_metadata_filename, 'w') as out:
    out.write(
        'node_id' + '\t' + 'node_namespace' + '\t' + 'node_label' + '\t' + 'node_definition' + '\t' + 'node_synonyms' + '\t' + 'node_dbxrefs' + '\n')

    for index, row in df_sk.iterrows():
        if index > 0:  # non-header
            node_id = str(row['code'])
            node_namespace = 'HubMAP'
            node_label = row['term']
            node_definition = str(row['definition'])
            node_synonyms = str(row['synonyms'])
            if not pd.isna(node_synonyms):
                node_synonyms = ''
            node_dbxrefs = str(row['dbxrefs'])
            if not pd.isna(node_dbxrefs):
                node_dbxrefs = ''

            out.write(
                node_id + '\t' + node_namespace + '\t' + node_label + '\t' + node_definition + '\t' + node_synonyms + '\t' + node_dbxrefs + '\n')

# RELATION METADATA
# Create a row for each type of relationship.

relation_filename = './OWLNETS_relations.txt'
print('Building OWLNETS_node_metadata')
with open(relation_filename, 'w') as out:
    out.write(
        'relation_id' + '\t' + 'relation_namespace' + '\t' + 'relation_label' + '\t' + 'relation_definition' + '\n')

    for col in range(6, len(df_sk.columns)):
        colhead = df_sk.columns[col]
        # predicate_uri = colhead[colhead.find('(')+1:colhead.find(')')]
        predicate_uri = colhead

        relation_namespace = args.ontology

        relation_definition = ''
        # out.write(predicate_uri + '\t' + relation_namespace + '\t' + label + '\t' + relation_definition + '\n')
        out.write(predicate_uri + '\t' + relation_namespace + '\t' + predicate_uri + '\t' + relation_definition + '\n')
