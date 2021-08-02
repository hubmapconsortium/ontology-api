#!/bin/bash

USER=$1
PASSWD=$2
BOLT_URL=$3
IMPORT=$4

function test_cypher_query {
    echo 'match (n) return count(n);' | cypher-shell -u "${USER}" -p "${PASSWD}" -a "${BOLT_URL}" >/dev/null 2>&1
}

# Spin here till the neo4j cypher-shell successfully responds...
until test_cypher_query ; do
    echo '.'
    sleep 1
done

# Now load the constraints...
cypher-shell -u "${USER}" -p "${PASSWD}" -a "${BOLT_URL}" -f "${IMPORT}/set_constraints.cypher"

echo 'ok'
