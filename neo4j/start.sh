#!/bin/bash

# Neo4j installation directory.
NEO4J=/usr/src/app/neo4j

# Get the neo4j password from system environment variable, default to HappyG0at if not set
NEO4J_PASSWORD=${NEO4J_PASSWORD}

echo "NEO4J_PASSWORD: $NEO4J_PASSWORD"

# Set the initial password of the initial admin user ('neo4j')
# And remove the requirement to change password on first login
# Must be performed before starting up the database for the first time
echo "Setting the neo4j password as the value of NEO4J_PASSWORD environment variable: $NEO4J_PASSWORD"
$NEO4J/bin/neo4j-admin set-initial-password $NEO4J_PASSWORD

# Start the neo4j server
$NEO4J/bin/neo4j console
