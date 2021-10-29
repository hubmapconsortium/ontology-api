#!/bin/bash

# Print a new line and the banner
echo
echo "==================== ONTOLOGY-API ===================="

# This function sets DIR to the directory in which this script itself is found.
# Thank you https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself                                                                      
function get_dir_of_this_script () {
    SCRIPT_SOURCE="${BASH_SOURCE[0]}"
    while [ -h "$SCRIPT_SOURCE" ]; do # resolve $SCRIPT_SOURCE until the file is no longer a symlink
        DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" >/dev/null 2>&1 && pwd )"
        SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
        [[ $SCRIPT_SOURCE != /* ]] && SCRIPT_SOURCE="$DIR/$SCRIPT_SOURCE" # if $SCRIPT_SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" >/dev/null 2>&1 && pwd )"
    echo 'DIR of script:' $DIR
}

# Set the version environment variable for the docker build
# Version number is from the VERSION file
# Also remove newlines and leading/trailing slashes if present in that VERSION file
function export_version() {
    export ONTOLOGY_API_VERSION=$(tr -d "\n\r" < VERSION | xargs)
    echo "ONTOLOGY_API_VERSION: $ONTOLOGY_API_VERSION"
}


if [[ "$1" != "dev" && "$1" != "prod" ]]; then
    echo "Unknown build environment '$1', specify one of the following: dev|prod"
else
    if [[ "$2" != "start" && "$2" != "stop" && "$2" != "down" ]]; then
        echo "Unknown command '$2', specify one of the following: start|stop|down"
    else
        # Show the script dir
        get_dir_of_this_script

        # Export and show the version
        export_version

        if [ "$2" = "start" ]; then
            docker-compose -f docker-compose.deployment.api.yml -p ontology-api up -d
        elif [ "$2" = "stop" ]; then
            docker-compose -f docker-compose.deployment.api.yml -p ontology-api stop
        elif [ "$2" = "down" ]; then
            docker-compose -f docker-compose.deployment.api.yml -p ontology-api down
        fi
    fi
fi