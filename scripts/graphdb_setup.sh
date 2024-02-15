#!/bin/bash

set -euo pipefail

# Command line arguments
PATH_TO_ENV_FILE=$1
NEW_ADMIN_PASS=$2
RUN_USER_SETUP=$3

# Set the environment variables in the shell, to use in the script
source "${PATH_TO_ENV_FILE}"

# Extract just the database name
DB_NAME="${NB_GRAPH_DB#repositories/}"
NB_GRAPH_PORT_HOST=${NB_GRAPH_PORT_HOST:-7200}

# Get the directory of this script to be able to find the data-config_template.ttl file
SCRIPT_DIR=$(dirname "$0")


##### First time GraphDB setup #####

if [ "${RUN_USER_SETUP}" = "on" ]; then
    # 1. Change database admin password and allow only authenticated users access
    curl -X PATCH --header 'Content-Type: application/json' http://localhost:${NB_GRAPH_PORT_HOST}/rest/security/users/admin -d "{\"password\": \""${NEW_ADMIN_PASS}"\"}"
    curl -X POST --header 'Content-Type: application/json' -d true http://localhost:${NB_GRAPH_PORT_HOST}/rest/security

    # 2. Create a new database user
    curl -X POST --header 'Content-Type: application/json' -u "admin:${NEW_ADMIN_PASS}" -d @- http://localhost:${NB_GRAPH_PORT_HOST}/rest/security/users/${NB_GRAPH_USERNAME} <<EOF
    {
        "username": "${NB_GRAPH_USERNAME}",
        "password": "${NB_GRAPH_PASSWORD}"
    } 
EOF
fi


##### Database setup #####

# 3. Create and save custom configuration file for the new database
# TODO: Should we add a suffix to data-config.ttl for the db name?
sed 's/rep:repositoryID "my_db" ;/rep:repositoryID "'"${DB_NAME}"'" ;/' ${SCRIPT_DIR}/data-config_template.ttl > data-config.ttl

# 4. Create a new database and give newly created user access permission
# Assumes data-config.ttl is in the same directory as this script!
curl -X PUT -u "admin:${NEW_ADMIN_PASS}" http://localhost:${NB_GRAPH_PORT_HOST}/${NB_GRAPH_DB} --data-binary "@data-config.ttl" -H "Content-Type: application/x-turtle"
curl -X PUT --header 'Content-Type: application/json' -d "
{\"grantedAuthorities\": [\"WRITE_REPO_${DB_NAME}\",\"READ_REPO_${DB_NAME}\"]}" http://localhost:${NB_GRAPH_PORT_HOST}/rest/security/users/${NB_GRAPH_USERNAME} -u "admin:${NEW_ADMIN_PASS}"
