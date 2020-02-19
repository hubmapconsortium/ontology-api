#!/bin/bash

if [[ "$1" != "dev" && "$1" != "test" ]]; then
	echo "Unknown build environment '$1', specify either 'dev' or 'test'"
else
	if [[ "$2" != "build" && "$2" != "start" && "$2" != "stop" ]]; then
		echo "Unknown command '$2', specify 'build', 'start' or 'stop' as the second argument"
	else
        if [ "$2" = "build" ]; then
			docker-compose -f docker-compose.$1.yml build
	    elif [ "$2" = "start" ]; then
			docker-compose -p ontology-neo4j-docker-$1 -f docker-compose.$1.yml up -d
		elif [ "$2" = "stop" ]; then
			docker-compose -p ontology-neo4j-docker-$1 -f docker-compose.$1.yml stop
	    fi
    fi
fi