#!/bin/bash

export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")

USER=neo4j

# Get the neo4j password and URI from system environment variable
NEO4J_PASSWORD=${NEO4J_PASSWORD}
NEO4J_URI=${NEO4J_URI}

echo "NEO4J_PASSWORD: $NEO4J_PASSWORD"
echo "NEO4J_URI: $NEO4J_URI"

# Run a simple query which (if it succeeds) tells us that the Neo4j is running...
function test_cypher_query {
    echo 'match (n) return count(n);' | cypher-shell -u "${USER}" -p "${NEO4J_PASSWORD}" -a "${NEO4J_URI}" --debug >/dev/null 2>&1
}

# Spin here till the neo4j cypher-shell successfully responds...
until test_cypher_query ; do
    echo '.'
    sleep 1
done

# Now load the constraints...
echo "Creating the constraints..."

cypher-shell -u "${USER}" -p "${NEO4J_PASSWORD}" -a "${NEO4J_URI}" --fail-at-end --debug -f "/usr/src/app/set_constraints.cypher"

echo 'ok'
