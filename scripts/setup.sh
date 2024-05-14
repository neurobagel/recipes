#!/bin/bash

/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=${NB_GRAPH_ROOT_CONT} &
GRAPHDB_PID=$!

export NB_GRAPH_ADMIN_PASSWORD=$(cat /run/secrets/db_admin_password)
export NB_GRAPH_PASSWORD=$(cat /run/secrets/db_user_password)

# Waiting for GraphDB to start
while ! curl --silent "localhost:${NB_GRAPH_PORT}/rest/repositories" -u "${NB_GRAPH_USERNAME}:${NB_GRAPH_PASSWORD}" | grep '\['; do
    :
done

# TODO: Do we also want to use this elsewhere in the script or stick to ./<some_path>?
SCRIPT_DIR=$(dirname "$0")
mkdir -p ${SCRIPT_DIR}/logs

# Logic for main setup
main() {
    echo "Setting up a Neurobagel graph backend..."
    echo -e "(The GraphDB server is being accessed inside the GraphDB container at http://localhost:${NB_GRAPH_PORT}.)\n"

    echo "Setting up GraphDB server..."
    ./graphdb_setup.sh --env-file-path /usr/src/neurobagel/.env "${NB_GRAPH_ADMIN_PASSWORD}"
    echo "Finished server setup."

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
