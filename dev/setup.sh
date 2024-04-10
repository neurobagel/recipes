#!/bin/bash

/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=/opt/graphdb/ &
GRAPHDB_PID=$!

# Waiting for GraphDB to start
while ! curl --silent "localhost:${NB_GRAPH_PORT_HOST}/rest/repositories" | grep '\[\]'; do
    :
done

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

main 2>&1 | tee -a ./DEPLOY.log

# We don't have jobcontrol here, so can't bring GraphDB back to foreground
# instead we'll wait
wait $GRAPHDB_PID
