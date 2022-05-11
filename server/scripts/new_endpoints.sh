#!/bin/bash
set -e
set -u

#SERVER=https://ontology-api.dev.hubmapconsortium.org
SERVER=https://ontology.api.hubmapconsortium.org

curl --verbose --request POST \
 --url $SERVER/concepts/expand \
 --header 'Content-Type: application/json' \
 --data '{
    "query_concept_id": "C2720507",
    "sab": ["SNOMEDCT_US", "HGNC"],
    "rel": ["isa", "isa"],
    "depth": 2
  }'
echo

curl --verbose --request POST \
 --url $SERVER/concepts/paths \
 --header 'Content-Type: application/json' \
 --data '{
    "query_concept_id": "C2720507",
    "sab": ["SNOMEDCT_US", "HGNC"],
    "rel": ["isa", "isa"]
  }'
echo

curl --verbose --request POST \
 --url $SERVER/concepts/shortestpaths \
 --header 'Content-Type: application/json' \
 --data '{
      "query_concept_id": "C2720507",
      "target_concept_id": "C1272753",
      "sab": ["SNOMEDCT_US", "HGNC"],
      "rel": ["isa", "part_of"]
  }'
echo

curl --verbose --request POST \
 --url $SERVER/concepts/trees \
 --header 'Content-Type: application/json' \
 --data '{
    "query_concept_id": "C2720507",
    "sab": ["SNOMEDCT_US", "HGNC"],
    "rel": ["isa", "isa"],
    "depth": 2
  }'
echo
