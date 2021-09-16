# Database building scripts

This section contains the scripts that are used to convert .owl files to .csv files that are then imported into a neo4j database.

This conversion is done in two stages and is coordinated by a build file.

Information is logged to a file './builds/logs/pkt_build_log.log'.

## Owls to OwlNets files

The './owlnets_script/__main__.py' is used to convert the Owls to OelNets (tab delimited files). Running this file with a '-h' parameter will give a list of arguments and optional arguments. This file is essentially the [PheKnowLator OWLNETS Example Application](https://github.com/callahantiff/PheKnowLator/blob/master/notebooks/OWLNETS_Example_Application.ipynb) with some additional housekeeping. It will download a file to './pkt_kg/libs/owltools' automatically.

It will process as follows:

### Owl Input

The .owl file is read from the web and stored in a './owl/***ontology***' directory (with the '.owl' extension). After that the MD5 of that file is computed and stored in a file with a .md5 extension in the same directory. The MD5 is compared on subsequent processing, and also serves as a part of the build manifest.

### Owlnets Output

The Oelnets files are written to the '/owlnets_output/***ontology***' directory. Subsequent processing is concerned with the three files of the form 'OWLNETS_*.txt'. These are tab delimited text files.

## Owlnets files to csv files

The Owlnets files are converted to .csv (comma delimited) files by the script located in './Jonathan/OWLNETS-UMLS-GRAPH.py'. This script takes it's input from the './owlnets_output' files, and a base set of [UMLS](https://www.nlm.nih.gov/research/umls/index.html) (.csv files) files. It writes to the '../neo4j/import/current' directory. It's changes are designed to be cumulative between runs, so when starting a run a freshly downloaded set of UMLS files should be placed there. The script that coordinates the running of this process will copy the current .csv files to a numbered save directory (e.g., 'save.1') so that the results of all iterations can be examined. In the end, it is only the final set of .csv files that is used as a basis for the neo4j graph.

## Coordination

The process is coordinated via the 'build_csv.sh' file which (after setting up a python environment) will run the build_csh.py file. The python virtual environment is placed in the './venv' directory using the './requirements.txt' file.

A prerequisite for running this file is that python3 be installed. It is also configured to run on a MAC currently.
