# HuBMAP Knowledge Graph Deployment Steps

## Prerequisites

**install git:** sudo yum install git

**install python3:** sudo yum install python3

**install mysql:**
sudo rpm -Uvh https://repo.mysql.com/mysql80-community-release-el7-3.noarch.rpm
sudo sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/mysql-community.repo
sudo yum --enablerepo=mysql80-community install mysql-community-server
**reset the default root password fro mysql:**
sudo service mysqld start
**find the default mysql password in the mysql log file:** sudo grep 'A temporary password' /var/log/mysqld.log
**reset the mysql root password:** 
login to mysql for first time follow prompts and set the root password to a new value (referred to as MYSQL_ROOT_PASSWORD in the rest of this document):
sudo mysql_secure_installation


**clone git repo:** git clone https://github.com/hubmapconsortium/ontology-api.git
move the ontology-api files to /opt/ontology-api

**install Java 11 (for neo4j):** downloaded Java 11 SE from Oracle's website (jdk-11.0.9_linux-x64_bin.rpm):
sudo rpm -ivh jdk-11.0.9_linux-x64_bin.rpm

**install neo4j**
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

**setup source directories**
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
PHEKNOWLATER_SOURCE_DIR = '/opt/ontology_files/pheknowlator_source_files'
CCF_SOURCE_DIR = '/opt/ontology_files/ccf_source_files'
TABLE_CREATE_SQL_FILEPATH = '/opt/ontology-api/src/neo4j_loader/sql/table_create.sql'
INDEX_CREATE_SQL_FILEPATH = '/opt/ontology-api/src/neo4j_loader/sql/add_indices.sql'
OUTPUT_DIR = '/opt/ontology_files/export'

# mysql connection
MYSQL_HOSTNAME = '127.0.0.1'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '<MYSQL_ROOT_PASSWORD>'
MYSQL_DATABASE_NAME = 'knowledge_graph'
```

**obtain source files**
* **UMLS Source Files:** The UMLS Source Files are exported from an Oracle installation of the UMLS Metathesaurus.  The instructions for doing this are found here: https://github.com/dbmi-pitt/UMLS-Graph/blob/master/CSV-Extracts.md.  Extract the files and move them to the UMLS_SOURCE_DIR directory in app.cfg (ex: /opt/ontology_files/umls_source_files.
* **PheKnowLator Source Files:** The PheKnowLator files are exported by running the software found here: https://github.com/callahantiff/PheKnowLator.  Specifically, this code needs 4 output files:
  * **edge_list file**- this file contains relationship data in the form of an RDF triple: subject, predicate, and object
  * **NodeMetdata file**- each ontology URI is represented in this file along with a label and definition
  * **Ontology_DbXRef file**- maps ontology URIs to other codes (ex: FMA, MeSH, etc.)
  * **relations file**- lists the relation URIs found in the edge_list with a label for each relation
* **CCF Source Files:** The CCF source files are available from HuBMAP personnel.  These files will most likely have an .OWL extension (same as RDF/XML).  This allows the file to be converted from RDF/XML to N-triples using RDFConverter.
  * **convert the ccf.owl to N-Triples (execute in /opt/rdfconvert-0.4/bin):** sudo ./rdfconvert.sh -i 'RDF/XML' -o 'N-Triples' /opt/ontology_files/ccf_source_files/ccf.owl /opt/ontology_files/ccf_source_files/ccf.nt
 


