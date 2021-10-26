#!/bin/sh

VENV=./venv

usage()
{
  echo "Usage: $0 [-r] [-R] [-v] [-h]"
  echo " -r Run server after building"
  echo " -R Reinstall VENV at ${VENV}"
  echo " -v Verbose output"
  echo " -h Help"
  exit 2
}

unset VERBOSE
while getopts 'rRvh' c; do
  echo "Processing $c : OPTIND is $OPTIND"
  case $c in
    r) RUN=true ;;
    R) REINSTALL=true ;;
    v) VERBOSE=true ;;
    h|?) usage ;;
  esac
done

shift $((OPTIND-1))

which python3
status=$?
if [[ $status != 0 ]] ; then
    echo '*** Python3 must be installed!'
    exit
fi

if [ $REINSTALL ]; then
  echo "Removing Virtual Environment located at ${VENV}"
  rm -rf ${VENV}
fi

if [[ ! -d ${VENV} ]] ; then
    echo "*** Installing python3 venv to ${VENV}"
    python3 -m pip install --upgrade pip
    python3 -m venv ${VENV}
    source ${VENV}/bin/activate
    pip install -r requirements.txt
    brew install wget
    # https://openapi-generator.tech/docs/generators/python-flask
    brew install openapi-generator
    echo "*** Done installing python3 venv"
fi

echo "*** Using python3 venv in ${VENV}"
source ${VENV}/bin/activate

openapi-generator generate -i ../ontology-openapi3.yaml -g python-flask -o .

./update_controller_and_manager.py

touch openapi_server/__init__.py

git checkout -- Dockerfile
git checkout -- requirements.txt

git add openapi_server/models
git add openapi_server/openapi/openapi.yaml
git add setup.py

# NOTE: setup.py has the wrong version should match that of the .yml file

if [ $RUN ]; then
  ./run_server_on_localhost.py
fi
