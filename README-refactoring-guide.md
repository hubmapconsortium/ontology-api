# Knowledge Base ETL Workflow Refactoring

## Introduction
This document explains how the current ETL Process for loading the Knowledge Base should be refactored.  The process will start with the UMLS .CSV files loaded using these steps: https://github.com/dbmi-pitt/UMLS-Graph/blob/master/CSV-Extracts.md.  These files form the UMLS basis for the rest of the process.

## Prerequisites
There are 5 file structures used by the refactored code.  These files follow a format initially developed by the PheKnowLator project.  **PLEASE NOTE: These files cannot contain any extra information.  The load process assumes there is no further filtering required to process this data.  Some errors may occur if extra entities or relations are found within the data.** The files and formats are presented below:  
* **node metadata**- This file contains a list of the "main entities" within the data.  These will include: genes, anatomic locations, proteins, diseases, etc.  There should only be one entry for each entity in this file.  This file includes the follwing columns:
  * **ontology_uri**- this column contains a unique identifier for the entity (typically an ontology URI).  This identifier is found in other files like the dbxref and edge list file.
  * **codeid**- this column contains an SAB prefix plus a code for the **ontology_uri** (ex: FMA 12345, MSH OU812).  This column will be parsed to set the **code** properties in the neo4j graph.  **IMPORTANT: For *ontology_uris* matching existing codes, this column must match the existing code (ex: FMA 12345, MSH OU812).**
  * **node_label**- the 'preferred term' for the entity.  
  * **node_definition**- a definition for the entity.
* **dbxref**- This file contains a list of cross-references for each **ontology_uri**.  The cross-references are a pipe-delimited list.  The individual cross-references adhere to a `<prefix> <identifier>` format.   
  * **ontology_uri**- the same unique identifier as found int the **node metadata** file.
  * **dbxrefs**- a pipe-delimited list of cross references (ex: `FMA 67860|BTO 0004185`).  **IMPORTANT: this column must match the existing codes.**
* **edge list**- This file contains relations between two **ontology_uri** identifiers.  A single **ontology_uri** can be found multiple times in this file.  The file format follows the N-triples from RDF: `subject   predicate   object .` where each line expresses a single statement.  Each statement can be read like a short English sentence.  For example, `UBERON_xyz has_part    UBERON_abc` reads "UBERON_xyz has a part UBERON_abc".
  * **subject**- The first identifier of the statement. It is the thing "owning" the predicate.  The same unique identifier as found int the **node metadata** file.
  * **predicate**- The relationship between the subject and object (ex: has_part, regulates, etc.).  The predicate is a URI found in the **relations** file.
  * **object**- The second identifier in the statement.  It is the target of the predicate.  
* **synonym list**- This file contains a list of **ontology_uri** and a list of strings representing the **ontology_uri's** synonyms.  In this file, the **ontology_uri** will repeat on several lines if there are multiple synonyms.  **PLEASE NOTE: Do not include any preferred terms in this file.  Only include synonyms.**    
  * **ontology_uri** the same unique identifier as found int the **node metadata** file.
  * **synonym** the synonym for the **ontology_uri**
* **relations** This file has a single entry for each unique **predicate** found in the **edge_list** file.  It also provides an English label for each relation.
  * **relation_id** The URI for the relation.  The relation URI should only be found in the list once.
  * **relation_label** The English label for the relation.  

## Configuration File
The configuration file will direct the data load process.  The refactor modifies one existing setting  and adds 5 items to the configuration file.  The new configuration file expects all the ontology files to live in the same directory `ONTOLOGY_SOURCE_DIR`.  Prior versions of the configuration file had several separate locations for the ontology files.  The file adds 5 settings:
* EDGE_LIST_FILE_TABLE_INFO
* NODE_METADATA_FILE_TABLE_INFO
* DBXREF_FILE_TABLE_INFO
* SYNONYM_LIST_FILE_TABLE_INFO
* RELATIONS_FILE_TABLE_INFO  

Each of these settings contains an array with objects.  **The order of the objects is important.  The objects must be listed in the correct order for "layering" the data.  If ontology A depends on ontology B then ontology B must be listed first.**  Each object contains this information:
* **file_name**- The name of the file to load.
* **table_name**- The name of the table to create from the data in the file.
* **SAB**- The SAB to be used when loading this data.

An example of these 5 settings is below:
```
EDGE_LIST_FILE_TABLE_INFO = [{'table_name':'uberon_edge_list','file_name':'uberon_edge.txt','SAB':'UBERON'},
{'table_name':'cl_edge_list','file_name':'cl_edge.txt','SAB':'CL'}]
NODE_METADATA_FILE_TABLE_INFO = [{'table_name':'uberon_node_metadata','file_name':'uberon_node_metadata.txt','SAB':'UBERON'},
{'table_name':'cl_node_metadata','file_name':'cl_node_metadata.txt','SAB':'CL'}]
DBXREF_FILE_TABLE_INFO = [{'table_name':'uberon_dbxref','file_name':'uberon_dbxref.txt','SAB':'UBERON'},
{'table_name':'cl_dbxref','file_name':'cl_dbxref.txt','SAB':'CL'}]
SYNONYM_FILE_TABLE_INFO = [{'table_name':'uberon_synonym_list','file_name':'uberon_synonym.txt','SAB':'UBERON'},
{'table_name':'cl_dbxref','file_name':'cl_dbxref.txt','SAB':'CL'}]
RELATIONS_FILE_TABLE_INFO = [{'table_name':'uberon_relations','file_name':'uberon_relations.txt','SAB':'UBERON'},
{'table_name':'cl_relations','file_name':'cl_relations.txt','SAB':'CL'}]
```  

## Code Workflow
### Extract Step
The `extract(config)` method in `load_csv_data.py` changes a bit.  The `load_umls_xxx(config)` methods remain in place.  Five new methods are added to `extract(config)`: `load_edge_list`, `load_node_metadata`, `load_dbxref`, `load_synonym_list`, and `load_relations`.  These five methods do the same thing:
1.  Create a for loop using one of the configuration items (EDGE_LIST_FILE_TABLE_INFO, NODE_METADATA_FILE_TABLE_INFO, etc.)
2.  Use the table_name and file_name from each object as parameters for the `load_file(config, file_path, table_name)` method

The `load_file(config, file_path, table_name)` needs to be updated to create the table for the table_name parameter.  The table creation will vary depending on the type of file being loaded (ex: edge_list, node_metadata, etc.)  

The `create_indices(config)` method needs to change.  It should use the 5 new configuration items (EDGE_LIST_FILE_TABLE_INFO, NODE_METADATA_FILE_TABLE_INFO, etc.) as parameters.  It will use these table_names to create indices for the tables created from the configuration files.  

The `build_xref_table(config)` method should be moved to the `transform(config)` method since it is really a transform step.

The new `extract(config)` method should look like this:
```
    create_database(config)
    load_node_metadata(config)
    load_relations(config)
    load_dbxref(config)
    load_edge_list(config)
    load_synonym_list(config)
    load_umls_codes(config)
    load_umls_defs(config)
    load_umls_suis(config)
    load_umls_cuis(config)
    load_umls_tuis(config)
    load_umls_cui_codes(config)
    load_umls_code_suis(config)
    load_umls_cui_cuis(config)
    load_umls_cui_suis(config)
    load_umls_cui_tuis(config)
    load_umls_def_rel(config)
    load_umls_tui_rel(config)
    create_indices(config)
    print("Done with extract process")
```

### Transform Step
The `transform(config)` method changes quite a bit in the refactored code.  First, `build_xref_table(config)` is added to the start of the `transform(config)` method.  

### Load Step
The `load(config)` method does not change in the refactored code.