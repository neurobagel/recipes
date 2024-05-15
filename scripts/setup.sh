#!/bin/bash

/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=/opt/graphdb/home &
GRAPHDB_PID=$!

export NB_GRAPH_ADMIN_PASSWORD=$(cat /run/secrets/db_admin_password)
export NB_GRAPH_PASSWORD=$(cat /run/secrets/db_user_password)

# Waiting for GraphDB to start
while ! curl --silent "localhost:${NB_GRAPH_PORT}/rest/repositories" -u "${NB_GRAPH_USERNAME}:${NB_GRAPH_PASSWORD}" | grep '\['; do
    :
done

# We need to figure out if this is the first time the setup has been run
repo_response=$(curl --silent "localhost:${NB_GRAPH_PORT}/rest/repositories" -u "${NB_GRAPH_USERNAME}:${NB_GRAPH_PASSWORD}")
if [ "${repo_response}" = "[]" ]; then
    export FIRST_TIME_SETUP="on"
else
    export FIRST_TIME_SETUP="off"
fi

echo "First time setup: ${FIRST_TIME_SETUP}"

# TODO: Do we also want to use this elsewhere in the script or stick to ./<some_path>?
SCRIPT_DIR=$(dirname "$0")
mkdir -p ${SCRIPT_DIR}/logs

# Logic for main setup
main() {
    echo "Setting up a Neurobagel graph backend..."
    echo -e "(The GraphDB server is being accessed inside the GraphDB container at http://localhost:${NB_GRAPH_PORT}.)\n"

    if [ "${FIRST_TIME_SETUP}" = "on" ]; then
        echo "Setting up GraphDB server..."
        ./graphdb_setup.sh --env-file-path /usr/src/neurobagel/.env "${NB_GRAPH_ADMIN_PASSWORD}"
        echo "Finished server setup."export FIRST_TIME_SETUP="on"
    else
        echo "GraphDB server already set up, skipping setup."
    fi

    echo "Adding datasets to the database..."
    ./add_data_to_graph.sh /data localhost:${NB_GRAPH_PORT} ${NB_GRAPH_DB} "${NB_GRAPH_USERNAME}" "${NB_GRAPH_PASSWORD}" --clear-data
    echo "Finished adding datasets to databases."

    echo "Adding Neurobagel vocabulary to the database"
    ./add_data_to_graph.sh ../vocab localhost:${NB_GRAPH_PORT} ${NB_GRAPH_DB} "${NB_GRAPH_USERNAME}" "${NB_GRAPH_PASSWORD}"
    echo "Finished adding the Neurobagel vocabulary to the database."

    echo "Finished setting up the Neurobagel graph backend."
}

main 2>&1 | tee -a ${SCRIPT_DIR}/logs/DEPLOY.log

# We don't have jobcontrol here, so can't bring GraphDB back to foreground
# instead we'll wait
wait $GRAPHDB_PID
