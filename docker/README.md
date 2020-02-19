# neo4j-docker

We have two versions of the neo4j: `dev` and `test`. The `dev` version is used for development related activities with a sample neo4j database. The `test` version is used for testing purposes before production deployment. And for both versions, the neo4j configuration and graph database are mounted from the host to the container for data persistence across container restarts.

## Set the neo4j password

The username for connecting to neo4j (via either neo4j browser or bolt protocol) is "neo4j" (can't change this) and default password is "1234". To change the neo4j password, go to `dev/start.sh` or `test/start.sh` and edit the line:

````
/usr/src/app/neo4j/bin/neo4j-admin set-initial-password 1234
````

## Build docker image and spin up the neo4j container

We'll describe the steps with `dev` version:

````
sudo chmod +x neo4j-docker.sh
sudo ./neo4j-docker.sh dev build
````

This build creates the neo4k docker image for `dev`. After that, we can start the neo4j container by:

````
sudo ./neo4j-docker.sh dev start
````

And to stop the service:

````
sudo ./neo4j-docker.sh dev stop
````

For testing deployment, simply change to:

`sudo ./neo4j-docker.sh test build` to build the docker image. Then `sudo ./neo4j-docker.sh test start` and `sudo ./neo4j-docker.sh test stop` for start and stop the neo4j `test` container.

The changes for `test` version include:

* Binding to different ports on the host.
* Run an `init` inside each container that forwards signals and reaps processes.
* Specifying a restart policy like `restart: always` to avoid downtime.

## Update base image

Both the `dev` and `test` versions are based on the `hubmap/neo4j-base-image:latest` image. If you need to update the base image, recrerate it with 

````
sudo docker build -t hubmap/neo4j-base-image:latest
````

Then publish it to the DockerHub:

````
sudo docker login
sudo docker push hubmap/neo4j-base-image:latest
````