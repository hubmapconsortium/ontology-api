# Scripts used by the Ontology Knowledge Graph Architecture

## Background
The application architecture that supports the HuBMAP ontology service 
includes a knowledge graph representing a polyhierarchical organization of 
interconnected ontologies. The knowledge graph is based on an export from the UMLS Metathesaurus, 
which manages the majority of the standard ontologies and vocabularies in the system. The distinctive feature of 
the HubMAP ontology is that it extends the UMLS knowledge by integrating concepts from other ontologies. 
In particular, the ontology includes information from sources such as: 
* Ontologies that are not in UMLS, but published in other sources such as the [OBO Foundry](https://obofoundry.org/) and the [NCBO BioPortal](https://bioportal.bioontology.org/) 
* Custom application ontologies, such as the ontology built for HuBMAP configuration information
* Data sources that can be represented as ontologies, such as the [UniProtKB](https://www.uniprot.org/) protein database.

The foundation of the ontology graph is a set of CSV files obtained 
from a MetamorPhoSys download of UMLS concept and semantic data. This initial set
of CSVs is enhanced with additions of data from other ontologies.

[This presentation](https://docs.google.com/presentation/d/1fTGVvTE5nziAMNt21wupmbkF1-X2GvW5Uhk26svaRvQ/edit?usp=sharing) i
describes:
* the overall solution architecture
* the process for obtaining the initial UMLS CSV files

The scripts in this folder path are used to convert data from ontologies into 
formats that can be appended to the set of UMLS CSV files.

The integration of an ontology into the complete set requires two stages 
for each ontology. The process is coordinated by a build file.

### Stage 1
Source data from an ontology is converted into the [OWLNETS](https://github.com/callahantiff/PheKnowLator/wiki/OWL-NETS-2.0) format. 
OWLNETs files represent ontologies as simple subject-predicate-object triples and metadata.

* For ontologies that are described in OWL files, the architecture uses the PheKnowLator package, as
described below, to extract OWL file content to OWLNETS format.
* For ontologies that are not described with OWL files (e.g., HUBMAP, UNIPROTKB), custom 
converters create files that conform to the OWLNETS format.

### Stage 2
The OWLNETS-UMLS-GRAPH script, described below, converts data from the OWLNETS files
into content that can be integrated into the base UMLS CSV structure.

### Logging

Information is logged to a file './builds/logs/pkt_build_log.log'.

# Running build_csv.sh to generate the CSV files 

To add an ontology, include an appropriate parameter to the 
command line of the build script--e.g.,
```
$ cd scripts
$ ./build_csv.sh -v PATO UBERON CL DOID CCFASCTB OBI EDAM HSAPDV SBO MI CHEBI MP ORDO PR UO HUSAT HUBMAP UNIPROTKB
```
The CSV files can be enhanced iteratively by calling the script successively.
For example, two calls to the script

```
./build_csv.sh -v PATO
./build_csv.sh -v UBERON
```

are equivalent to the call that combines the arguments
```
./build_csv.sh -v PATO UBERON
```

### Run times by ontology
The approximate complete run time for creating the CSV files associated with 15 ontologies is 
about 26 hrs on a MacBook Pro 2.6 GHz 6-core I7 /w 32 GB 2667 MHz memory.

Sample times per ontology:
* PATO: 1 minute
* UBERON: 4 minutes
* CL: 3 minutes
* DOID: 2 minutes
* CCFASCTB: 1 minute
* OBI: 1 minute
* EDAM: 1 minute
* HSAPDV: 1 minute
* SBO: 1 minute
* MI: 1 minute
* **CHEBI: 8 hours**
* MP: 8 minutes
* ORDO: 6 minutes
* **PR: 11 hours**
* HUSAT: 1 minute
* HUBMAP: 1 minute
* UNIPROTKB: 5 minutes

### Regenerating without downloading or OWLNETS conversion
Once the complete script has been run on the local machine, it is possible 
to rerun the build script without downloading source files (e.g, OWL files) 
or running the OWL-OWLNETS conversion scripts again. This avoids the need
to obtain source data for ontologies that do not update often.

A number of parameters in the
build_csv.**py** script (called by the build_csv.**sh** shell script) control processing.

### Order of ontology integration
Nodes in an ontologies can refer to nodes in other ontologies in two ways:
1. Via **relationships**--e.g., a node for a protein in UNIPROTKB has a _gene product of_ relationship with a gene node in HGNC.
2. Via **equivalence classes** (cross-references)--e.g., a node in HUBMAP may be equivalent to a node in OBI.

If an ontology refers to nodes in another ontology, the referred ontology nodes should be defined 
one of two places:
#### 
1. The OWLNETS_node_metadata.txt file of the ontology. (For example, the PATO ontology refers to nodes in ontologies like CHEBI, but defines them with distinct IRIs in the node metadata.)
2. The ontology CSV files--in particular, CUI-CODES.CSV.

In other words, relationships between ontologies determines the order in which they are integrated.

The recommended order of generation follows. 
* PATO 
* UBERON 
* CL 
* DOID 
* CCFASCTB 
* OBI 
* EDAM 
* HSAPDV 
* SBO 
* MI 
* CHEBI 
* MP 
* ORDO 
* PR 
* UO 
* HUSAT 
* HUBMAP 
* UNIPROTKB

The order appears to be of particular importance for custom ontologies such as HUBMAP and UNIPROTKB.

### ontology.json

The file 'scripts/ontologies.json' is used to specify information about the ontologies (e.g., source url, the associated SAB).
The key of the JSON object is used on the command line of the build_csv.sh script.

The JSON file allows for both the conversion of OWL-based files and custom conversion.

## OWL to OWLNETS files

The './owlnets_script/__main__.py' is used to convert OWL files to OWLNETS format (tab delimited files).
Running this file with a '-h' parameter will give a list of arguments and optional arguments.
This file is essentially the [PheKnowLator OWLNETS Example Application](https://github.com/callahantiff/PheKnowLator/blob/master/notebooks/OWLNETS_Example_Application.ipynb) with some additional housekeeping.
It will download a file to './pkt_kg/libs/owltools' automatically.

It will process as follows:

### OWL Input

The .OWL file is read from the web and stored in the './owl/***ontology***' directory (with the '.owl' extension).
After that the MD5 of that file is computed and stored in a file with a .md5 extension in the same directory.
The MD5 is compared on subsequent processing, and also serves as a part of the build manifest.
If the computed MD5 does not match the MD5 found in the .md5 file, an error is generated; in general this should not happen.

### OWLNETS Output

The OWLNETS files are written to the '/owlnets_output/***ontology***' directory.
Subsequent processing is concerned with the three files of the form 'OWLNETS_*.txt'.
These are tab delimited text files that are read by the 'OWLNETS-UMLS-GRAPH.py' program.

## OWLNETS files to CSV files

The OWLNETS files are converted to .CSV (comma delimited) files by the script located in './Jonathan/OWLNETS-UMLS-GRAPH.py'.
This script takes its input from the './owlnets_output/' files, and a base set of [UMLS](https://www.nlm.nih.gov/research/umls/index.html) (.csv files) files.
It writes to the '../neo4j/import/current' directory.
Its changes to the files in that directory are cumulative between runs, so when starting a run a freshly downloaded set of UMLS files should be placed there.
The script that coordinates the running of this process will copy the current .csv files to a numbered save directory (e.g., 'save.1') so that the results of intermediate iterations can be examined.
In the end, it is only the final set of .csv files that is used as a basis for the neo4j graph.

### Adding command line arguments to OWLNETS-UMLS-GRAPH.py

(JAS 13 October 2022 - Deprecated. Changes are now made directly to 
OWLNETS-UMLS-GRAPH12.py.)

~~The 'OWLNETS-UMLS-GRAPH.py' is generated from the notebook 'OWLNETS-UMLS-GRAPH.ipynb' found in the same directory.
In order to make the 'OWLNETS-UMLS-GRAPH.py' functional for this processing, a transform script 'transorm.py' is run over it.
This script will allow it to take command line parameters necessary for processing here.~~

## Coordination

The process is coordinated via the 'build_csv.sh' file which (after setting up a python environment) will run the build_csh.py file where the logic is located.
The python virtual environment is placed in the './venv' directory using the './requirements.txt' file.

A prerequisite for running this file is that python3 be installed. It is also configured to run in OSX (MacBook Pro) currently.

### Processing

The 'build_csv.py' file takes an optional parameter '-h' which allows you to see other parameters.
In general it runs a loop over the Owl URI list specified in the 'OWL_URLS' variable, processing each Owl file as follows:
1. Run the 'owlnets_script/__main__.py' program over the OWL file after downloading it to the 'owl/&lt;OWL&gt;/' directory, and generating the .md5 file associated with it in that directory.
2. Copy the .csv files found in '../neo4j/import/current' to a save directory at the same level (e.g., 'save.3/).
3. Run the 'Jonathan/OWLNETS-UMLS-GRAPH.py' over the owlnets_script generated files in the 'owlnets_output/&lt;OWL&gt;/' directory. This will modify the .csv files found in the '../neo4j/import/current' with the output from step 1. for the Owl file processed there.

This process repeats until all of the OWL files are processed.
The resulting .csv files can then be used to create a new Neo4j database (see the README.md file in the neo4j directory).

### Listing the OWL files (ontologies) that will be in Knowledge Graph database

Currently (as stated previously) there is a variable 'OWL_URLS' in the 'build_csv.py' file that lists the Owl files that will be included in list order.

In addition to this list, there is a 'owl_sab' parameter to the 'OWLNETS-UMLS-GRAPH.py' script which is usually the name of the owl file. In instances where this is not the case, the 'owl_sab' variable must be special cased. This is done at line 247.
