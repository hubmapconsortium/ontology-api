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

There should be two docker images for the Ontology server on this machine. NEVER EVER touch any other images that you may find!
```buildoutcfg
$ docker images
REPOSITORY                       TAG       IMAGE ID       CREATED        SIZE
ontology-api_neo4j-constraints   latest    5618329cf6ca   11 hours ago   690MB
ontology-api_ontology-neo4j      latest    1ea152e3d19c   11 hours ago   9.01GB
```

The neo4j container should be running. The neo4j-constraints container will most likely not be running because it simply runs till it has processed its constraints and then exits; it has a very short life span.
```buildoutcfg
$ docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED        STATUS                  PORTS                                                                                  NAMES
c49e97df99ec   ontology-api_ontology-neo4j   "/usr/src/app/start.…"   11 hours ago   Up 11 hours (healthy)   0.0.0.0:7477->7474/tcp, :::7477->7474/tcp, 0.0.0.0:7688->7687/tcp, :::7688->7687/tcp   ontology-neo4j
```

Stop the deployed server, and notice that there is also an associated volume which needs to be deleted.
```buildoutcfg
$ docker-compose -f docker-compose.deployment.neo4j.yml down
NOTE: After this the 'ontology-api_ontology-neo4j' will not show up when running 'docker ps'
$ docker volume ls -q
$ docker volume rm ontology-api_ontology-neo4j-data
ontology-api_ontology-neo4j-data
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

Determine that there are two new images, one for the neo4j server and another for the neo4j-constraints setting process.
```buildoutcfg
$ docker images
REPOSITORY                       TAG       IMAGE ID       CREATED          SIZE
ontology-api_neo4j-constraints   latest    3477b597b514   34 seconds ago   690MB
ontology-api_ontology-neo4j      latest    54a08940394d   35 seconds ago   9.57GB
...
```

Start both containers so that they detach.
```buildoutcfg
$ docker-compose -f docker-compose.deployment.neo4j.yml up -d
Creating network "ontology-api_ontology-neo4j-network" with the default driver
Creating volume "ontology-api_ontology-neo4j-data" with default driver
Creating ontology-neo4j ... done
Creating neo4j-constraints ... done
```

You should find something like this running. It is unlikely that you will see the neo4j-constraints server running because it's life span is so short.
```buildoutcfg
$ docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS                    PORTS           \
                                                                       NAMES
60e02ed00622   ontology-api_ontology-neo4j   "/usr/src/app/start.…"   41 minutes ago   Up 41 minutes (healthy)   0.0.0.0:7477->74\
74/tcp, :::7477->7474/tcp, 0.0.0.0:7688->7687/tcp, :::7688->7687/tcp   ontology-neo4j
...
```

Delete any of the old images; the ones with TAG == &lt;none&gt; with *docker rmi IMAGE ID*. For example....
```buildoutcfg
$ docker images
REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
ontology-api_neo4j-constraints   latest    3477b597b514   8 minutes ago   690MB
ontology-api_ontology-neo4j      latest    54a08940394d   8 minutes ago   9.57GB
<none>                           <none>    c88d789593e8   6 days ago      690MB
<none>                           <none>    effe59e7decd   6 days ago      9.28GB
...

$ docker rmi c88d789593e8
$ docker rmi effe59e7decd
```

Look at the logs for the 'ontology-api_neo4j-constraints' container. It's last line should be 'ok'!
```buildoutcfg
$ docker ps -a
CONTAINER ID   IMAGE                            COMMAND                  CREATED       STATUS                   PORTS                                                        \
                          NAMES
a43206d75fde   ontology-api_neo4j-constraints   "./load_constraints.…"   5 hours ago   Exited (0) 5 hours ago                                                                \
                          neo4j-constraints
0b23257cc291   ontology-api_ontology-neo4j      "/usr/src/app/start.…"   5 hours ago   Up 5 hours (healthy)     0.0.0.0:7477->7474/tcp, :::7477->7474/tcp, 0.0.0.0:7688->7687\
/tcp, :::7688->7687/tcp   ontology-neo4j

$ docker logs a43206d75fde
NEO4J_PASSWORD: HappyG0at
NEO4J_URI: bolt://ontology-neo4j:7687
....
Creating the constraints...
ok
$
```

At this point you can check to see if you can hit the server from the web interface, and if so you are done!

:-)
