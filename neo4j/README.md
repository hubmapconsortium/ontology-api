# Neo4j Ontology database

The database is always build "from scratch" using the .csv files created by the process run in the './scripts' directory. Here this rebuild process is discussed.

## Rebuilding

Copy the data (.csv) files to neo4j deployment machine (host).
```buildoutcfg
$ cd ~/Documents/Git/ontology-api/neo4j/import/current
$ mkdir -p tmp/current; cp *.csv tmp/current
$ CSV_TIMESTAMP=$(date +"%Y%m%d_%H%M")
$ (cd ./tmp; tar zcfv ../../current_${CSV_TIMESTAMP}.tgz .)
$ scp -i ~/.ssh/id_rsa_e2c.pem ../current_${CSV_TIMESTAMP}.tgz cpk36@neo4j.dev.hubmapconsortium.org:/tmp
$ rm -rf ./tmp
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
$ tar zxfv /tmp/current_&lt;CSV_TIMESTAMP&gt;.tgz
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
Stopping ontology-neo4j ... done
Removing ontology-neo4j ... done
Removing network ontology-api_ontology-neo4j-network
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

The ontology data is being mounted from the ontology-neo4j container to the host VM using named volume: `ontology-neo4j-data`.
We need to delete the old volume mount before starting the container of the new image:
```
docker volume inspect ontology-api_ontology-neo4j-data
docker volume rm ontology-api_ontology-neo4j-data
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
...
Starting Neo4j.
Started neo4j (pid 135). It is available at http://localhost:7474/
There may be a short delay until the server is ready.
See /usr/src/app/neo4j/logs/neo4j.log for current status.
Waiting for server to begin fielding Cypher queries...
Cypher Query available waiting...
Cypher Query available waiting...
...
Creating the constraints using Cypher queries...
Picked up _JAVA_OPTIONS: -XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0
0 rows available after 11644 ms, consumed after another 0 ms
Deleted 527771 nodes
0 rows available after 720 ms, consumed after another 0 ms
Added 1 constraints
...
Sleeping for 2m to allow the indexes to be built before going to read_only mode...
Stopping neo4j server to go into read_only mode...
Only allow read operations from this Neo4j instance...
Restarting neo4j server in read_only mode...
Directories in use:
  home:         /usr/src/app/neo4j
  config:       /usr/src/app/neo4j/conf
  logs:         /usr/src/app/neo4j/logs
  plugins:      /usr/src/app/neo4j/plugins
  import:       /usr/src/app/neo4j/import
  data:         /usr/src/app/neo4j/data
  certificates: /usr/src/app/neo4j/certificates
  run:          /usr/src/app/neo4j/run
Starting Neo4j.
Picked up _JAVA_OPTIONS: -XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0
2021-09-30 21:00:26.867+0000 INFO  Starting...
2021-09-30 21:00:28.974+0000 INFO  ======== Neo4j 4.2.5 ========
2021-09-30 21:00:36.669+0000 INFO  Performing postInitialization step for component 'security-users' with version 2 and status CURRENT
2021-09-30 21:00:36.670+0000 INFO  Updating the initial password in component 'security-users'  
2021-09-30 21:00:42.552+0000 INFO  Called db.clearQueryCaches(): Query cache already empty.
2021-09-30 21:00:42.621+0000 INFO  Bolt enabled on 0.0.0.0:7687.
2021-09-30 21:00:43.625+0000 INFO  Remote interface available at http://localhost:7474/
2021-09-30 21:00:43.626+0000 INFO  Started.
^C
```

Optionally, remove the database files from /tmp.
```buildoutcfg
$ exit
$ rm /tmp/current_&lt;CSV_TIMESTAMP&gt;.tgz
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
