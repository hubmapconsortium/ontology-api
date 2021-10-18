#!/bin/sh

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

VENV=./venv
which python3
status=$?
if [[ $status != 0 ]] ; then
    echo '*** Python3 must be installed!'
    exit
fi

if [[ ! -d ${VENV} ]] ; then
    echo "*** Installing python3 venv to ${VENV}"
    python3 -m pip install --upgrade pip
    python3 -m venv ${VENV}
    source ${VENV}/bin/activate
    pip install -r requirements.txt
    brew install wget
    echo "*** Done installing python3 venv"
fi

echo "*** Using python3 venv in ${VENV}"
source ${VENV}/bin/activate

# https://openapi-generator.tech/docs/generators/python-flask
brew install openapi-generator

openapi-generator generate -i ../ontology-openapi3.yaml -g python-flask -o .
./update_controller_and_manager.py

touch openapi_server/__init__.py

git checkout -- Dockerfile
git checkout -- requirements.txt

# NOTE: setup.py has the wrong version should match that of the .yml file

# ./run_server_on_localhost.py
