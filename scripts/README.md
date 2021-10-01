# Database building scripts

This section contains the scripts that are used to convert .owl files to .csv files that are then imported into a neo4j database.

This conversion is done in two stages and is coordinated by a build file.

Information is logged to a file './builds/logs/pkt_build_log.log'.

## Owls to OwlNets files

The './owlnets_script/__main__.py' is used to convert the Owls to OelNets (tab delimited files). Running this file with a '-h' parameter will give a list of arguments and optional arguments. This file is essentially the [PheKnowLator OWLNETS Example Application](https://github.com/callahantiff/PheKnowLator/blob/master/notebooks/OWLNETS_Example_Application.ipynb) with some additional housekeeping. It will download a file to './pkt_kg/libs/owltools' automatically.

It will process as follows:

### Owl Input

The .owl file is read from the web and stored in the './owl/***ontology***' directory (with the '.owl' extension). After that the MD5 of that file is computed and stored in a file with a .md5 extension in the same directory. The MD5 is compared on subsequent processing, and also serves as a part of the build manifest. If the computed MD5 does not match the MD5 found in the .md5 file, an error is generated; in general this should not happen.

### Owlnets Output

The Oelnets files are written to the '/owlnets_output/***ontology***' directory. Subsequent processing is concerned with the three files of the form 'OWLNETS_*.txt'. These are tab delimited text files that are read by the 'OWLNETS-UMLS-GRAPH.py' file.

## Owlnets files to csv files

The Owlnets files are converted to .csv (comma delimited) files by the script located in './Jonathan/OWLNETS-UMLS-GRAPH.py'. This script takes it's input from the './owlnets_output/' files, and a base set of [UMLS](https://www.nlm.nih.gov/research/umls/index.html) (.csv files) files. It writes to the '../neo4j/import/current' directory. It's changes are cumulative between runs, so when starting a run a freshly downloaded set of UMLS files should be placed there. The script that coordinates the running of this process will copy the current .csv files to a numbered save directory (e.g., 'save.1') so that the results of all iterations can be examined. In the end, it is only the final set of .csv files that is used as a basis for the neo4j graph.

### Adding command line arguments to OWLNETS-UMLS-GRAPH.py

The 'OWLNETS-UMLS-GRAPH.py' is generated from the notebook 'OWLNETS-UMLS-GRAPH.ipynb' found in the same directory. In order to make the 'OWLNETS-UMLS-GRAPH.py' functional for this processing, a transform script 'transorm.py' is run over it. This script will allow it to take command line parameters necessary for processing here.

## Coordination

The process is coordinated via the 'build_csv.sh' file which (after setting up a python environment) will run the build_csh.py file where the logic is located. The python virtual environment is placed in the './venv' directory using the './requirements.txt' file.

A prerequisite for running this file is that python3 be installed. It is also configured to run on a MAC currently.

### Processing

The 'build_csv.py' file takes an optional parameter '-h' which allows you to see other parameters. In general it runs a loop over the Owl URI list specified in the 'OWL_URLS' variable, processing each Owl file as follows:
1. Run the 'owlnets_script/__main__.py' program over the Owl file after downloading it to the 'owl/&lt;OWL&gt;/' directory, and generating the .md5 file associated with it in that directory.
2. Copy the .csv files found in '../neo4j/import/current' to a save directory at the same level (e.g., 'save.3/).
3. Run the 'Jonathan/OWLNETS-UMLS-GRAPH.py' over the owlnets_script generated files in the 'owlnets_output/&lt;OWL&gt;/' directory. This will modify the .csv files found in the '../neo4j/import/current' with the output from step 1. for the Owl file processed there.

This process repeats until all of the Owl files are processed. The resulting .csv files can then be used to create a new Neo4j database (see the README.md file in the neo4j directory).

### Listing the Oel files (ontologies) that will be in Knowledge Graph database

Currently (as stated previously) there is a variable 'OWL_URLS' in the 'build_csv.py' file that lists the Owl files that will be included in list order.

In addition to this list, there is a 'owl_sab' parameter to the 'OWLNETS-UMLS-GRAPH.py' script which is usually the name of the owl file. In instances where this is not the case, the 'owl_sab' variable must be special cased. This is done at line 247.
