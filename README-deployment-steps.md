# HuBMAP Knowledge Graph Deployment Steps

The HuBMAP Knowledge Graph is deployed to ont-build.dev.hubmapconsortium.org

## Prerequisites

**install git:** sudo yum install git

**install python3:** sudo yum install python3

**install mysql:**  
sudo rpm -Uvh https://repo.mysql.com/mysql80-community-release-el7-3.noarch.rpm  
sudo sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/mysql-community.repo  
sudo yum --enablerepo=mysql80-community install mysql-community-server  
**reset the default root password for mysql:**  
sudo service mysqld start  
**find the default mysql password in the mysql log file:**   sudo grep 'A temporary password' /var/log/mysqld.log  
**reset the mysql root password:**  
login to mysql for first time follow prompts and set the root password to a new value (referred to as MYSQL_ROOT_PASSWORD in the rest of this document):  
sudo mysql_secure_installation  


**clone git repo:** git clone https://github.com/hubmapconsortium/ontology-api.git  
move the ontology-api files to /opt/ontology-api  

**install Java 11 (for neo4j):** downloaded Java 11 SE from Oracle's website (jdk-11.0.9_linux-x64_bin.rpm):  
sudo rpm -ivh jdk-11.0.9_linux-x64_bin.rpm  

**install neo4j (this code was tested with neo4j 4.1.4 and 4.1.5)**  
sudo rpm --import https://debian.neo4j.com/neotechnology.gpg.key  
sudo touch /etc/yum.repos.d/neo4j.repo  
sudo vi /etc/yum.repos.d/neo4j.repo  

add this section to **neo4j.repo**:  
[neo4j]  
name=Neo4j RPM Repository  
baseurl=https://yum.neo4j.com/stable  
enabled=1  
gpgcheck=1  

sudo yum install neo4j-4.1.4

**install unzip (for RDFConverter):** sudo yum install unzip 

**install RDFConverter (for CCF file):**  
download the 0.4 zip file from https://sourceforge.net/projects/rdfconvert/  
move rdfconvert-0.4-bin.zip to /opt  
unzip rdfconvert-0.4-bin.zip: sudo unzip rdfconvert-0.4-bin.zip  

## Setup Source Files

**Step 1: setup source directories**
in /opt: sudo mkdir ontology_files
under /opt/ontology_files make the following directories:
* umls_source_files
* pheknowlator_source_files
* ccf_source_files
* export

copy app.cfg.example to a new file called app.cfg: cp app.cfg.example app.cfg  
edit app.cfg:

```
UMLS_SOURCE_DIR = '/opt/ontology_files/umls_source_files'
ONTOLOGY_SOURCE_DIR = '/opt/ontology_files/pheknowlator_source_files'
TABLE_CREATE_SQL_FILEPATH = '/opt/ontology-api/src/neo4j_loader/sql/table_create.sql'
INDEX_CREATE_SQL_FILEPATH = '/opt/ontology-api/src/neo4j_loader/sql/add_indices.sql'
OUTPUT_DIR = '/opt/ontology_files/export'
EDGE_LIST_FILE_TABLE_INFO = [{'table_name':'uberon_edge_list','file_name':'uberon_edge_list.txt','sab':'UBERON'},
{'table_name':'cl_edge_list','file_name':'cl_edge_list.txt','sab':'CL'}]
NODE_METADATA_FILE_TABLE_INFO = [{'table_name':'uberon_node_metadata','file_name':'uberon_node_metadata.txt','sab':'UBERON'},
{'table_name':'cl_node_metadata','file_name':'cl_node_metadata.txt','sab':'CL'}]
DBXREF_FILE_TABLE_INFO = [{'table_name':'uberon_dbxref','file_name':'uberon_dbxref.txt','sab':'UBERON'},
{'table_name':'cl_dbxref','file_name':'cl_dbxref.txt','sab':'CL'}]
#SYNONYM_LIST_FILE_TABLE_INFO = [{'table_name':'ccf_synonym','file_name':'ccf_synonym.txt','sab':'CCF'}]
RELATIONS_FILE_TABLE_INFO = [{'table_name':'uberon_relation','file_name':'uberon_relations.txt','sab':'UBERON'},
{'table_name':'cl_relation','file_name':'cl_relations.txt','sab':'CL'}]

# mysql connection
MYSQL_HOSTNAME = '127.0.0.1'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '<MYSQL_ROOT_PASSWORD>'
MYSQL_DATABASE_NAME = 'knowledge_graph'
```

**Step 2: obtain source files**
* **UMLS Source Files:** The UMLS Source Files are exported from an Oracle installation of the UMLS Metathesaurus.  The instructions for doing this are found here: https://github.com/dbmi-pitt/UMLS-Graph/blob/master/CSV-Extracts.md.  Extract the files and move them to the UMLS_SOURCE_DIR directory in app.cfg (ex: /opt/ontology_files/umls_source_files.
* **PheKnowLator Source Files:** The PheKnowLator files are exported by running the software found here: https://github.com/callahantiff/PheKnowLator.  Specifically, this code needs 4 output files:
  * **edge_list file**- this file contains relationship data in the form of an RDF triple: subject, predicate, and object
  * **NodeMetdata file**- each ontology URI is represented in this file along with a label and definition
  * **Ontology_DbXRef file**- maps ontology URIs to other codes (ex: FMA, MeSH, etc.)
  * **relations file**- lists the relation URIs found in the edge_list with a label for each relation
* **CCF Source Files:** The CCF source files are available from HuBMAP personnel.  These files will most likely have an .OWL extension (same as RDF/XML).  This allows the file to be converted from RDF/XML to N-triples using RDFConverter.
  * **convert the ccf.owl to N-Triples (execute in /opt/rdfconvert-0.4/bin):** sudo ./rdfconvert.sh -i 'RDF/XML' -o 'N-Triples' /opt/ontology_files/ccf_source_files/ccf.owl /opt/ontology_files/ccf_source_files/ccf.nt  

**Step 3: copy relations files**
There are 2 relations files stored in the repo: cl_relations.txt and uberon_relations.txt.  These files contain the UBERON and Cell Ontology relations plus their inverse relations.  These files need to be copied from /opt/ontology-api/src/neo4j_loader to /opt/ontology_files/pheknowlator_source_files.
 
 **Step 4: pre-process source files**
 The pre_process_files.sh file splits the PheKnowLator files (which contain a superset of data) into their ontology-specific (UBERON, Cell Ontology, etc.) subset of files.  
 Edit the /opt/ontology-api/src/neo4j_loader/pre_process_files.sh file to reference the correct directories:  
 ```
cd /opt/ontology_files/pheknowlator_source_files
head -1 PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt > /opt/ontology_files/pheknowlator_source_files/cl_dbxref.txt
grep "^http://purl.obolibrary.org/obo/CL_" PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt >> /opt/ontology_files/pheknowlator_source_files/cl_dbxref.txt
head -1 PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt > /opt/ontology_files/pheknowlator_source_files/uberon_dbxref.txt
grep "^http://purl.obolibrary.org/obo/UBERON_" PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt >> /opt/ontology_files/pheknowlator_source_files/uberon_dbxref.txt
head -1 PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt > /opt/ontology_files/pheknowlator_source_files/cl_edge_list.txt
grep "^http://purl.obolibrary.org/obo/CL_" PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt >> /opt/ontology_files/pheknowlator_source_files/cl_edge_list.txt
head -1 PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt > /opt/ontology_files/pheknowlator_source_files/uberon_edge_list.txt
grep "^http://purl.obolibrary.org/obo/UBERON_" PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt >> /opt/ontology_files/pheknowlator_source_files/uberon_edge_list.txt
head -1 PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt > /opt/ontology_files/pheknowlator_source_files/cl_node_metadata.txt
grep "^http://purl.obolibrary.org/obo/CL_" PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt >> /opt/ontology_files/pheknowlator_source_files/cl_node_metadata.txt
head -1 PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt > /opt/ontology_files/pheknowlator_source_files/uberon_node_metadata.txt
grep "^http://purl.obolibrary.org/obo/UBERON_" PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt >> /opt/ontology_files/pheknowlator_source_files/uberon_node_metadata.txt

 ```
 
 After the file is edited, run it to build the new files:  
 ./pre_process_files.sh
 
 Edit the /opt/ontology_files/pheknowlator_source_files/uberon_node_metadata.txt and /opt/ontology_files/pheknowlator_source_files/cl_node_metadata.txt files:  
 There is an error in the pre_process_files.sh script.  The first columns are set to 'node_id'.  They need to be renamed 'ontology_uri'.
 
## Run Code
**install python dependencies (just run once)**  
cd to /opt/ontology-api/src/neo4j_loader  
install dependencies: sudo pip3 install -r requirements.txt  
**run extract step**  
pipe the output to a text file and run in background (it takes 5 hours to run):  
sudo python3 load_csv_data.py extract > extract_run.log &  
**run extract_non_umls step**  
This is an alternative to the 'extract' command.  It only loads the non-UMLS data.  This can 
greatly reduce the time required to reload the data.  This can only be used if the UMLS data has not changed since the last
time the 'extract' was run.  
sudo python3 load_csv_data.py extract_non_umls > extract_non_umls_run.log &  
**run transform step**  
pipe the output to a text file and run in background (it takes 15 minutes to run):  
sudo python3 load_csv_data.py transform > transform_run.log &  
**run load step**  
pipe the output to a text file and run in background (it takes 5 minutes to run):  
sudo python3 load_csv_data.py load > load_run.log &  
**optional step**  
The code allows you to run multiple commands are the same time.  So you can run this code to perform the entire process:  
sudo python3 load_csv_data.py extract transform load > full_process.log &  

## Populate neo4j Graph  
**Step 1: Edit /opt/ontology-api/src/neo4j_loader/reload_neo4j_data.sh**  
This file runs the neo4j commands to reload neo4j with the new data from the load step.  Edit the file so it looks like this:  
```
#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"
echo "Using $1 as the password for the neo4j user"

cd /var/lib/neo4j
sudo neo4j stop
sudo rm -rf data/databases/*
sudo rm -rf data/transactions/*
sudo rm -rf import/*
sudo cp /opt/ontology_files/export/* import
sudo cp /opt/ontology_files/umls_source_files/NDC* import
sudo chown neo4j:adm import/*
sudo neo4j-admin import --nodes=Semantic="import/TUIs.csv" --nodes=Concept="import/CUIs.csv" --nodes=Code="import/CODEs.csv" --nodes=Term="import/SUIs.csv" --nodes=Definition="import/DEFs.csv" --nodes=NDC="import/NDCs.csv" --relationships=ISA_STY="import/TUIrel.csv" --relationships=STY="import/CUI-TUIs.csv" --relationships="import/CUI-CUIs.csv" --relationships=CODE="import/CUI-CODEs.csv" --relationships="import/CODE-SUIs.csv" --relationships=PREF_TERM="import/CUI-SUIs.csv" --relationships=DEF="import/DEFrel.csv" --relationships=NDC="import/NDCrel.csv" --skip-bad-relationships --skip-duplicate-nodes
sudo neo4j-admin set-initial-password $1
sudo neo4j start
sleep 20
sudo cypher-shell -u neo4j -p $1 'MATCH (n:Term) WHERE size((n)--())=0 DELETE (n)'
sudo cypher-shell -u neo4j -p $1 -f /opt/ontology-api/src/neo4j_loader/cypher/create_neo4j_indices.cql
sudo cypher-shell -u neo4j -p $1 -f /opt/ontology-api/src/neo4j_loader/cypher/create_semantic_types.cql


```

**Step 2: Run /opt/ontology-api/src/neo4j_loader/reload_neo4j_data.sh**  
sudo ./reload_neo4j_data.sh 1234

