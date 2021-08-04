#!/bin/bash

export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")

USER=$1
PASSWD=$2
BOLT_URL=$3
IMPORT=$4

# Run a simple query which (if it succeeds) tells us that the Neo4j is running...
function test_cypher_query {
    echo 'match (n) return count(n);' | cypher-shell -u "${USER}" -p "${PASSWD}" -a "${BOLT_URL}" --debug >/dev/null 2>&1
}

# Spin here till the neo4j cypher-shell successfully responds...
until test_cypher_query ; do
    echo '.'
    sleep 1
done

# Now load the constraints...
cypher-shell -u "${USER}" -p "${PASSWD}" -a "${BOLT_URL}" --fail-at-end --debug -f "${IMPORT}/set_constraints.cypher"

echo 'ok'
