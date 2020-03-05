#!/bin/bash

#if [ -z "$1"] then 
#    echo "Missing 'neo4j' password argument.  Please run again and specify a password for the 'neo4j' account"
#	exit 1
#fi

echo "Load HuBMAP Ontology into Neo4j"

neo4j_home=/home/chb69/neo4j
neo4j_bin=/home/chb69/neo4j/bin
neo4j_import=/home/chb69/neo4j/import
neo4j_data=/home/chb69/neo4j/data
csv_home_directory=/home/chb69/git/ontology-api/import/umls_data
ontology_api_directory=/home/chb69/git/ontology-api
version_node_label="UMLS Data"

# NOTE: You need to execute the neo4j-admin command from the Neo4j home directory
#otherwise, the neo4j-admin command cannot find the import directories
cd $neo4j_home

# start neo4j if it is not already running (to reset the password)
$neo4j_bin/neo4j start

echo "Stopping Neo4j"
$neo4j_bin/neo4j stop

echo "Deleting Existing Neo4j Data"
rm -rf $neo4j_data/*

echo "Cleaning Neo4j import directory"
rm -rf $neo4j_import/*
cp -r $csv_home_directory $neo4j_import

echo "Importing Data"

`$neo4j_home/bin/neo4j-admin import --nodes:Semantic "import/umls_data/TUIs.csv" --nodes:Concept "import/umls_data/CUIs.csv" --nodes:Code "import/umls_data/CODEs.csv" --nodes:Term "import/umls_data/SUIs.csv" --nodes:Definition "import/umls_data/DEFs.csv" --relationships:ISA_STY "import/umls_data/TUIrel.csv" --relationships:STY "import/umls_data/CUI-TUIs.csv" --relationships "import/umls_data/CUI-CUIs.csv" --relationships "import/umls_data/CUI-CODEs.csv" --relationships "import/umls_data/CODE-SUIs.csv" --relationships:PREF_TERM "import/umls_data/CUI-SUIs.csv" --relationships:DEF "import/umls_data/DEFrel.csv" --ignore-missing-nodes`

echo "Starting Neo4j"
$neo4j_bin/neo4j start

echo "Setting 'Neo4j' Account Password"
$neo4j_bin/neo4j-admin set-initial-password $1

# sleep to allow the Neo4j system to fully launch
sleep 30

echo "Running Cypher cleanup queries"
cypher_cleanup_cql_file=$ontology_api_directory/src/cleanup.cql
#maybe pass some arguments here to use when building the "version" node
cat $cypher_cleanup_cql_file | $neo4j_bin/cypher-shell -u neo4j -p $1
$neo4j_bin/cypher-shell -u neo4j -p $1 "CREATE (v:Version {timestamp : timestamp(), label: '$version_node_label'});"

#stop Neo4j and copy the data files into the github repository
echo "Stopping Neo4j"
$neo4j_bin/neo4j stop

echo "Copying Neo4j source files to github repo"
rm -rf $ontology_api_directory/docker/dev/graph.db
cp -r $neo4j_data/databases/graph.db $ontology_api_directory/docker/dev


echo "Done"
