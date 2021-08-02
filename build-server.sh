#!/bin/sh

# https://openapi-generator.tech/docs/generators/python-flask
# brew install openapi-generator
# https://editor.swagger.io/
SERVER_DIR=server
BACKUP_EXT=bak
if [[ -d $SERVER_DIR ]]; then
    rm -rf ${SERVER_DIR}.${BACKUP_EXT}
    mv $SERVER_DIR ${SERVER_DIR}.${BACKUP_EXT}
fi
openapi-generator generate -i ontology-0.0.1.yaml -g python-flask -o $SERVER_DIR
files=`find . -name *.py -exec grep -l "from openapi_server" {} \;`
#for f in $files; do
#    sed -i .$BACKUP_EXT "s/from openapi_server/from ${SERVER_DIR}.openapi_server/g" $f
#done
#sed -i .$BACKUP_EXT "s/x-openapi-router-controller: openapi_server/x-openapi-router-controller: ${SERVER_DIR}.openapi_server/g" ${SERVER_DIR}/openapi_server/openapi/openapi.yaml
#sed -i .$BACKUP_EXT "s/^connexion\[swagger-ui\] >= 2.6.0; .*$/connexion[swagger-ui] >= 2.6.0/g" ${SERVER_DIR}/requirements.txt
