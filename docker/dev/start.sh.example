#!/bin/bash

# Set JAVA_HOME
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:/bin/java::")

# Set the password for native user `neo4j` (must be performed before starting up the database for the first time)
/usr/src/app/neo4j/bin/neo4j-admin set-initial-password 1234

# Use `console` instead of `start` to keep the terminal window stay open
/usr/src/app/neo4j/bin/neo4j console
