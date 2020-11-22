#!/bin/bash

if [ "$1" = "build" ]; then
			docker-compose -f docker-compose.yml build
elif [ "$1" = "start" ]; then
			docker-compose -p ontology-neo4j-docker -f docker-compose.yml up -d
elif [ "$1" = "stop" ]; then
			docker-compose -p ontology-neo4j-docker -f docker-compose.yml stop

fi
