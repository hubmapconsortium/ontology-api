# Neo4j Ontology database

The database is always build "from scratch" using the .csv files created by the process run in the './scripts' directory. Here this rebuild process is discussed.

## Rebuilding

Copy the data (.csv) files to neo4j deployment machine (host).
```buildoutcfg
$ cd ~/Documents/Git/ontology-api/neo4j/import/current
$ mkdir -p tmp/current; cp *.csv tmp/current
$ (cd tmp; tar zcfv ../current.tgz .)
$ scp -i ~/.ssh/id_rsa_e2c.pem current.tgz cpk36@neo4j.dev.hubmapconsortium.org:/tmp
$ rm -rf ~/tmp
```

Go to the host and update from the repository.
```buildoutcfg
$ ssh -i ~/.ssh/id_rsa_e2c.pem cpk36@neo4j.dev.hubmapconsortium.org
$ sudo /bin/su - centos
$ cd hubmap/ontology-api
# NOTE: this is a Git reposntory https://github.com/hubmapconsortium/ontology-api.git so make sure that you are in the right branch...
$ git pull
```

Delete the old database import files (.csv) and install the new ones.
```buildoutcfg
$ pushd neo4j/import
$ rm -rf current
$ tar zxfv /tmp/current.tgz
$ popd
$ rm /tmp/current.tgz
```

The neo4j container should be running.
```buildoutcfg
$ docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED        STATUS                  PORTS                                                                                  NAMES
c49e97df99ec   ontology-api_ontology-neo4j   "/usr/src/app/start.…"   11 hours ago   Up 11 hours (healthy)   0.0.0.0:7477->7474/tcp, :::7477->7474/tcp, 0.0.0.0:7688->7687/tcp, :::7688->7687/tcp   ontology-neo4j
```

Stop the deployed server, and notice that there is also an associated volume which needs to be deleted.
```buildoutcfg
$ docker-compose -f docker-compose.deployment.neo4j.yml down
NOTE: After this the 'ontology-api_ontology-neo4j' will not show up when running 'docker ps'
$ docker volume rm ontology-api_ontology-neo4j-data
ontology-api_ontology-neo4j-data
```

Delete the old image. NEVER EVER touch any other images that you may find!
```buildoutcfg
$ docker images
REPOSITORY                    TAG       IMAGE ID       CREATED        SIZE
ontology-api_ontology-neo4j   latest    5944de80ab13   2 hours ago    9.3GB
...
$ docker rmi 5944de80ab13
```

Rebuild the container.
```buildoutcfg
$ docker-compose -f docker-compose.deployment.neo4j.yml build --no-cache
Building ontology-neo4j
...
IMPORT DONE in 2m 23s 351ms.
Imported:
  19991810 nodes
  51537255 relationships
  77104970 properties
Peak memory usage: 1.289GiB
There were bad entries which were skipped and logged into /usr/src/app/neo4j/bin/import.report
...
Successfully built 0ace526b088f
Successfully tagged ontology-api_ontology-neo4j:latest
```

Determine that there is a new images for the neo4j server.
```buildoutcfg
$ docker images
REPOSITORY                       TAG       IMAGE ID       CREATED          SIZE
ontology-api_ontology-neo4j      latest    54a08940394d   35 seconds ago   9.57GB
...
```

Start the container.
```buildoutcfg
$ docker-compose -f docker-compose.deployment.neo4j.yml up -d
Creating network "ontology-api_ontology-neo4j-network" with the default driver
Creating volume "ontology-api_ontology-neo4j-data" with default driver
Creating ontology-neo4j ... done
```

You should find something like this running.
```buildoutcfg
$ docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS                    PORTS                                                                                  NAMES
60e02ed00622   ontology-api_ontology-neo4j   "/usr/src/app/start.…"   41 minutes ago   Up 41 minutes (healthy)   0.0.0.0:7477->7474/tcp, :::7477->7474/tcp, 0.0.0.0:7688->7687/tcp, :::7688->7687/tcp   ontology-neo4j
...
```

Look at the logs for the server.
```buildoutcfg
$ docker logs -f 60e02ed00622
```

At this point you can check to see if you can hit the server from the web interface
```buildoutcfg
http://neo4j.dev.hubmapconsortium.org:7477/browser/
```

Find a code:
```buildoutcfg
MATCH (c:Code) where ID(c)=13824345 RETURN c
```

Try to delete the code:
```buildoutcfg
MATCH (c:Code) where ID(c)=13824345 DELETE c
ERROR SessionExpired
No longer possibe to write to server at	neo4j.dev.hubmapconsortium.org:7688
```

You are done! :-)
