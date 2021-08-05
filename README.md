# HuBMAP Ontology API

The HuBMAP Ontology API contains a Neo4j graph loaded with the [UMLS](https://www.nlm.nih.gov/research/umls/index.html).  The UMLS allows extensive cross-referencing across many biomedical vocabulary systems.  The UMLS structure will form the basis for the rest of the ontologies added into this system.  The backbone of the UMLS data is the Concept to Concept relationship (aka the UMLS CUI to CUI).  The UMLS Concept provides an anchor for the various vocabularies and ontologies.  The user can "walk" backbone of the graph in a vocabulary agnostic manner and/or branch off into specific voabularies.

There are three pieces/containers here:
* The neo4j server that contains the onthology which is build with .csv files on startup. The .csv files are not stored in the git repo because some are covered by licenses. The .csv files will be deleted when the server is built to save disk space on the server.
* Constraints need to be added to the data in the neo4j database, but that can only be done after it is up and running. The neo4j-constraints container will wait for the neo4j server to start to take commands and then run a batch of constraints to 'fixup' the databse making it ready to be used.
* The server container is a RESTful API server that is created by the 'build-serer.sh' script from the 'ontology-x.x.x.yml' OpenAPI specification file. There is an additional 'server/openapi_server/controllers/neo4j_manager.py' that is used to define neo4j queries that are used by the endpoints in a one-to-one manner. From this YAML file it is also possible to create clients for the server that can be included in programs acessing the serer.

## Local Deployment Instructions

* Create an 'import' directory under the 'neo4j' that contains the CSV files that should be imported into the neo4j database by the 'neo4j-admin' program in the Docker file.
* Run the file 'docker-compose build --no-cache' which will create the three containers described above.
* After the containers are built, run 'docker-compose up' to start all three containers. When the 'neo4j-constraints' container has finished the database will have been build.

## Use it Instructions

* The URL 'http://<<host>>:8080/ui/' will render an interface from which the OPENapi endpoints can be viewed and tested.

## Remote Deployment

### Deploy Neo4j services

On the VM where the `ontology-neo4j` and `ontology-neo4j-constraints` services will be running:

````
docker-compose -f docker-compose.deployment.neo4j.yml up -d
````

### Deploy ontology-api

First need to configure `ontology-api/server/openapi_server/resources/app.properties` with the correct neo4j connection information, in order to connect to the `ontology-neo4j` container running on another VM.

On the VM where the `ontology-api` service will be running:

````
docker-compose -f docker-compose.deployment.api.yml up -d
````

## Data persistence

The ontology data is being mounted from the `ontology-neo4j` container to the host VM using named volume: `ontology-neo4j-data`, which is defiened in the `docker-compose.deployment.neo4j.yml`. 

To locate the mountpoint on the host file system, run:
````
docker volume inspect ontology-api_ontology-neo4j-data
````