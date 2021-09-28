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
```

The neo4j container should be running.
```buildoutcfg
$ docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED        STATUS                  PORTS                                                                                  NAMES
c49e97df99ec   ontology-api_ontology-neo4j   "/usr/src/app/start.…"   11 hours ago   Up 11 hours (healthy)   0.0.0.0:7477->7474/tcp, :::7477->7474/tcp, 0.0.0.0:7688->7687/tcp, :::7688->7687/tcp   ontology-neo4j
```

Stop the container, and notice that there is also an associated volume which needs to be deleted.
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

Rebuild the container. The warning about 'bad entries' is normal.
```buildoutcfg
$ docker-compose -f docker-compose.deployment.neo4j.yml build --no-cache
Building ontology-neo4j
Sending build context to Docker daemon  3.252GB
...
IMPORT DONE in 2m 12s 946ms. 
Imported:
  20355207 nodes
  51956018 relationships
  78267224 properties
Peak memory usage: 1.292GiB
There were bad entries which were skipped and logged into /usr/src/app/neo4j/bin/import.report
...
Successfully built 0ace526b088f
Successfully tagged ontology-api_ontology-neo4j:latest
```

Determine that there is a new image.
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

Look at the logs for the container. You should see it waiting for "Cypher Query available", and then it will create constraints using Cypher queries. After this it will sleep for a minute of two, shurdown, change the database to read_only and then restart the database.
```buildoutcfg
$ docker logs -f 60e02ed00622
```

Optionally, remove the database files from /tmp.
```buildoutcfg
$ exit
$ rm /tmp/current.tgz
$ exit
logout
Connection to neo4j.dev.hubmapconsortium.org closed.
```

## Checking

At this point you can check to see if you can hit the neo4j server from the web interface. Change the "Connect URL" port to 7688.
```buildoutcfg
http://neo4j.dev.hubmapconsortium.org:7477/browser/
```

Find a code, then click on the code to get the &lt;id&gt;.
```buildoutcfg
MATCH (c:Code) RETURN c LIMIT 1
```

Try to delete the code using the &lt;id&gt; as follows. You should see the following error message because you cannot modify the neo4j database since it has been deployed in read_only mode.
```buildoutcfg
MATCH (c:Code) where ID(c)=13824345 DELETE c
ERROR SessionExpired
No longer possibe to write to server at	neo4j.dev.hubmapconsortium.org:7688
```

You are done! :-)
