# HuBMAP Ontology API

The HuBMAP Ontology API contains a Neo4j graph loaded with the [UMLS](https://www.nlm.nih.gov/research/umls/index.html).  The UMLS allows extensive cross-referencing across many biomedical vocabulary systems.  The HuBMAP Ontology API will use UMLS as a starting framework to connect the various HuBMAP specific ontologies with other biomedical vocabulary systems.  Eventually this code will include a set of API calls to retrieve vocabulary information.  Currently, the system only consists of an exposed Neo4j graph.  

## Deployment Instructions

### Local dev deployment

Currently, there is only a development version of this API. To build it check out the code from this git repository.  These steps assume you have docker deployed and running on your machine.  Next follow these steps:
````
cd docker
./neo4j-docker.sh dev start
````

Note: you may need to execute ./neo4j-docker.sh dev start using the sudo command depending on your docker configuration.

After deploying the code, the Neo4j endpoint should be accessible through http://localhost:7474.  This should present you with a Neo4j browser interface.
