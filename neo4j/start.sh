#!/bin/bash

# Neo4j installation directory.
NEO4J=/usr/src/app/neo4j

# Get the neo4j password and URI from system environment variable
NEO4J_USER=${NEO4J_USER}
NEO4J_PASSWORD=${NEO4J_PASSWORD}

echo "NEO4J_USER: $NEO4J_USER"
echo "NEO4J_PASSWORD: $NEO4J_PASSWORD"

# Run a simple query which (if it succeeds) tells us that the Neo4j is running...
function test_cypher_query {
    echo 'match (n) return count(n);' | cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" >/dev/null 2>&1
}

# Set the initial password of the initial admin user ('neo4j')
# And remove the requirement to change password on first login
# Must be performed before starting up the database for the first time
echo "Setting the neo4j password as the value of NEO4J_PASSWORD environment variable: $NEO4J_PASSWORD"
$NEO4J/bin/neo4j-admin set-initial-password $NEO4J_PASSWORD

echo "Start the neo4j server in the background..."
$NEO4J/bin/neo4j start

# Spin here till the neo4j cypher-shell successfully responds...
echo "Waiting for server to begin fielding Cypher queries..."
until test_cypher_query ; do
    echo '.'
    sleep 1
done

echo "Creating the constraints using Cypher queries..."
# https://neo4j.com/docs/operations-manual/current/tools/cypher-shell/
cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASSWORD}" --format verbose --fail-at-end --debug -f "/usr/src/app/set_constraints.cypher"

echo "Stopping neo4j server..."
# https://neo4j.com/developer/kb/how-to-properly-shutdown-a-neo4j-database/
if [[! "${bin/neo4j stop}"]]; then
  while [["${bin/neo4j status}"]];
    sleep 1
    echo "Still waiting..."
  done;
fi

echo "Only allow read operations from this Neo4j instance..."
# https://neo4j.com/docs/operations-manual/current/configuration/neo4j-conf/#neo4j-conf
echo "dbms.read_only=true" >> ${NEO4J}/conf/neo4j.conf

echo "Restarting neo4j server..."
# Docker requires your command to keep running in the foreground. Otherwise, it thinks that your applications stops and shutdown the container.
$NEO4J/bin/neo4j console
