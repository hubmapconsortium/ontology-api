# HuBMAP Ontology API

The HuBMAP Ontology API contains a Neo4j graph loaded with the [UMLS](https://www.nlm.nih.gov/research/umls/index.html).  The UMLS allows extensive cross-referencing across many biomedical vocabulary systems.  The UMLS structure will form the basis for the rest of the ontologies added into this system.  The backbone of the UMLS data is the Concept to Concept relationship (aka the UMLS CUI to CUI).  The UMLS Concept provides an anchor for the various vocabularies and ontologies.  The user can "walk" backbone of the graph in a vocabulary agnostic manner and/or branch off into specific voabularies.

The HuBMAP Ontology API consists of four pieces:
* Code to load UMLS and ontologies into Neo4j
* Neo4j graph containing UMLS plus other ontologies
* Web service interface into the Neo4j graph ***coming soon***
* Docker containers for the web service and graph ***coming soon***


## Deployment Instructions

### Current Deployment
REQUIREMENTS: MySQL 14.14 and Neo4j 4.1.4 

The executable code in src/neo4j_loader/load_csv_data.py is directed by a file called app.cfg:

* UMLS_SOURCE_DIR the directory containing the source UMLS source CSV files
* PHEKNOWLATER_SOURCE_DIR the directory containing the PheKnowLator tab-delimited files (the UBERON and Cell Ontology sources)
* TABLE_CREATE_SQL_FILEPATH the filepath to the file used to create the tables in mysql (ontology-api/src/neo4j_loader/sql/table_create.sql)
* INDEX_CREATE_SQL_FILEPATH the filepath to the file used to create indices in mysql (ontology-api/src/neo4j_loader/sql/add_index.sql)
* OUTPUT_DIR the directory where the updated CSV files will be created.
* MySQL and Neo4j settings

To run the code, comment out the extract(config), transform(config), and load(config) depending on what piece you wish to run.
* extract(config) this takes the data from UMLS_SOURCE_DIR and PHEKNOWLATER_SOURCE_DIR and loads it into the MySQL database.  This takes a long period of time to run (approx. 2-3 hours).
* transform(config) this merges the UMLS data, UBERON, and Cell Ontoloogy into a new set of MySQL tables
* load(config) this dumps the MySQL data into a new set of CSV files for loading into Neo4j

The /ontology-api/src/neo4j_loader/reload_neo4j_data.sh script helps load a Neo4j graph with the data from the OUTPUT_DIR.
