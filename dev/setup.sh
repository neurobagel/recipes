#!/bin/bash

/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=/opt/graphdb/ &
GRAPHDB_PID=$!

# Waiting for GraphDB to start
while ! curl --silent "localhost:${NB_GRAPH_PORT_HOST}/rest/repositories" | grep '\[\]'; do
    :
done

# TODO: Do we also want to use this elsewhere in the script or stick to ./<some_path>?
SCRIPT_DIR=$(dirname "$0")

# Logic for main setup
main() {
    echo -e "Setting up a Neurobagel graph backend...\n"

    echo "Setting up GraphDB server..."
    ./graphdb_setup.sh "${NB_GRAPH_ADMIN_PASSWORD}"
    echo "Finished server setup."

    echo "Adding datasets to the database..."
    ./add_data_to_graph.sh ./data localhost:${NB_GRAPH_PORT_HOST} ${NB_GRAPH_DB} "${NB_GRAPH_USERNAME}" "${NB_GRAPH_PASSWORD}"
    echo "Finished adding datasets to databases."

    echo "Adding Neurobagel vocabulary to the database"
    ./add_data_to_graph.sh ./vocab localhost:${NB_GRAPH_PORT_HOST} ${NB_GRAPH_DB} "${NB_GRAPH_USERNAME}" "${NB_GRAPH_PASSWORD}"
    echo "Finished adding the Neurobagel vocabulary to the database."

    echo "Finished setting up the Neurobagel graph backend."
}

main 2>&1 | tee -a ${SCRIPT_DIR}/DEPLOY.log

# We don't have jobcontrol here, so can't bring GraphDB back to foreground
# instead we'll wait
wait $GRAPHDB_PID
