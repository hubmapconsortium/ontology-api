#!/bin/bash

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

OWL_NETS_SCRIPT='./owl_nets_script/__main__.py'
VALIDATION_SCRIPT='./blackbox_validation/__main__.py'

# https://uberon.github.io/downloads.html
# Use the simpler one first....
UBERON_OWL_URL='http://purl.obolibrary.org/obo/uberon.owl'
# Use this data (the extended version)...
UBERON_EXT_OWL_URL='http://purl.obolibrary.org/obo/uberon/ext.owl'

# This should get relationships and inverses and the RO code where we want the name...
# http://www.obofoundry.org/ontology/ro.html
# ro_url = 'http://purl.obolibrary.org/obo/ro.owl'

# http://www.obofoundry.org/ontology/cl.html
# Complete ontology, plus inter-ontology axioms, and imports modules
CL_OWL_URL='http://purl.obolibrary.org/obo/cl.owl'

# http://www.obofoundry.org/ontology/chebi.html
CHEBL_OWL_URL='http://purl.obolibrary.org/obo/chebi.owl'

# BREAKS
# http://www.obofoundry.org/ontology/pr.html
PRO_OWL_URL='http://purl.obolibrary.org/obo/pr.owl'

# http://www.obofoundry.org/ontology/pato.html
PATO_OWL_URL='http://purl.obolibrary.org/obo/pato.owl'

DOID_OWL_URL='http://purl.obolibrary.org/obo/doid.owl'

OBI_OWL_URL='http://purl.obolibrary.org/obo/obi.owl'

CCF_OWL_URL='https://ccf-ontology.hubmapconsortium.org/ccf.owl'

OWL_URLS=($UBERON_OWL_URL $CL_OWL_URL $CHEBL_OWL_URL $PRO_OWL_URL $PATO_OWL_URL $DOID_OWL_URL $OBI_OWL_URL $CCF_OWL_URL)

usage() {
  cat << EOF
Usage: $0 [ -h ] [ -d ] [ -v ] [ -u url ] [ -s ]
Process the default OWL files with black box validation after processing
each OWL file.
-h      Display this and exit
-d      List the default OWL files to process and exit
-v      Verbose mode on
-u url  Process this OWL url instead of the default list and then exit
-s      Skip the black box validation
EOF
}

VERBOSE=0
VALIDATION=1
URL=
# https://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts "h?dvu:" opt; do
  case "$opt" in
    h|\?)
      usage
      exit 2
      ;;
    d)
      echo -n "Default OWLs to process: ${OWL_URLS[*]}" >&2
      echo "" >&2
      exit 0
      ;;
    v)
      echo "Verbose mode enabled" >&2
      VERBOSE=1
      ;;
    u)
      URL=$OPTARG
      echo "Using single URL ${URL}" >&2
      ;;
    s)
      echo "Skip black box validation" >&2
      VALIDATION=0
      ;;
  esac
done

shift $((OPTIND-1))
# first_nonopt_arg=$1

VENV=./venv
which python3
status=$?
if [[ $status != 0 ]] ; then
    echo '*** Python3 must be installed!'
    exit
fi

if [[ -d ${VENV} ]] ; then
    echo "*** Using python3 venv in ${VENV}"
    source ${VENV}/bin/activate
else
    echo "*** Installing python3 venv to ${VENV}"
    python3 -m venv ${VENV}
    source ${VENV}/bin/activate
    pip install -r requirements.txt
    brew install wget
    echo "*** Done installing python3 venv"
fi

if [[ -n $URL ]] ; then
    $OWL_NETS_SCRIPT "$URL"
    status=$?
    exit $?
fi

for url in ${OWL_URLS[*]}; do
    echo "*** Running $OWL_NETS_SCRIPT"
    $OWL_NETS_SCRIPT "$url"
    if [[ $VALIDATION -eq 1 ]] ; then
        $VALIDATION_SCRIPT
    fi
done
