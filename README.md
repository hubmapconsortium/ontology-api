# HuBMAP Ontology API

The HuBMAP Ontology API contains a Neo4j graph loaded with the [UMLS](https://www.nlm.nih.gov/research/umls/index.html).
The UMLS allows extensive cross-referencing across many biomedical vocabulary systems.
The UMLS structure will form the basis for the rest of the ontologies added into this system.
The backbone of the UMLS data is the Concept to Concept relationship (aka the UMLS CUI to CUI).
The UMLS Concept provides an anchor for the various vocabularies and ontologies.
The user can "walk" backbone of the graph in a vocabulary agnostic manner and/or branch off into specific vocabularies.

The API documentation on SmartAPI: https://smart-api.info/ui/dea4bf91545a51b3dc415ba37e2a9e4e

There are two containers here:

* The `ontology-neo4j` container that contains the ontology which is build with .csv files on startup. The .csv files are not stored in the git repo because some are covered by licenses. The .csv files will be deleted when the server is built to save disk space on the server.

* The `ontology-api` container is a RESTful API server that is created by the 'build-serer.sh' script from the 'ontology-x.x.x.yml' OpenAPI specification file. There is an additional 'server/openapi_server/controllers/neo4j_manager.py' that is used to define neo4j queries that are used by the endpoints in a one-to-one manner. From this YAML file it is also possible to create clients for the server that can be included in programs acessing the serer.

## Local Development Instructions

For local development, [HuBMAP Gateway](https://github.com/hubmapconsortium/gateway) is not needed, simply following the below steps:

* Create an `import` directory under the `neo4j` that contains the CSV files that should be imported into the neo4j database by the 'neo4j-admin' program in the Docker file.
* Under the project root directory, run command `docker-compose -f docker-compose.localhost.yml build --no-cache` which will create the two container images described above.
* After the images are built, run `docker-compose -f docker-compose.localhost.yml up` to start the two containers.


Once the containers are ready, they can be accessed at:

- `ontology-api`: `http://localhost:8080/`
- `ontology-neo4j`: `http://localhost:7474` and the default username is `neo4j` with password `HappyG0at`


## Remote Deployment on DEV and PROD

When deploying the ontology services on the DEV and PROD, we'll use the `ontology-api` docker image that has been
pre-built and published to DockerHub: https://hub.docker.com/r/hubmap/ontology-api.
The `ontology-api` will also be running behind the [HuBMAP Gateway](https://github.com/hubmapconsortium/gateway).
The `ontology-neo4j` image can not be published to DockerHub, so we'll always need to build it on the deployment VM. 

### Publish ontology-api docker image

First we need to build a released version of the `ontology-api` image locally, specify the `latest` tag as well as
the new version tag based on the version number in `VERSION` file, for example:
```
cd server
docker build -t hubmap/ontology-api:latest -t hubmap/ontology-api:1.1.1 .
```

Then publish this image with the the `latest` tag as well as the released version tag to DockerHub:
```
docker login
docker push hubmap/ontology-api:latest
docker push hubmap/ontology-api:1.1.1
```

### Deploy ontology-api

First we need to create a new configuration file `ontology-api/server/openapi_server/resources/app.properties` with 
the correct neo4j connection information, in order to connect to the `ontology-neo4j` container running on another VM.

On the VM where the `ontology-api` service will be running:
````
Usage: ./ontology-api-docker-deployment.sh [dev|prod] [start|stop|down]
````

### Deploy ontology-neo4j

On the VM where the `ontology-neo4j` service will be running, have the CSV files placed under `neo4j/import/current`, then run
````
docker-compose -f docker-compose.deployment.neo4j.yml up -d
````

This will create the docker image and spin up the neo4j container as well, the process will take some time.

## Data persistence

The ontology data is being mounted from the `ontology-neo4j` container to the host VM using named volume: `ontology-neo4j-data`, which is defiened in the `docker-compose.deployment.neo4j.yml`. 

To locate the mountpoint on the host file system, run:
````
docker volume inspect ontology-api_ontology-neo4j-data
````

## Publish OpenAPI file on SmartApi

There is a HubMap account on SmartApi that allows you to publish OpenAPI specked files after you set this up.
Once done the file will be automatically updated upon checkin.
