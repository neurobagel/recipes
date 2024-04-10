#!/bin/bash

echo "Setting up a Neurobagel graph backend..."

/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=/opt/graphdb/ &
GRAPHDB_PID=$!

# Waiting for GraphDB to start
while ! curl --silent "localhost:7200/rest/repositories" | grep '\[\]'; do
    :
done

echo "Running GraphDB server setup..."
./graphdb_setup.sh apple
echo "Finished server setup."

echo "Adding datasets to the database..."
./add_data_to_graph.sh ./data localhost:7200 repositories/my_db DBUSER DBPASSWORD
echo "Finished adding datasets to databases."

echo "Adding Neurobagel vocabulary to the database"
./add_data_to_graph.sh ./vocab localhost:7200 repositories/my_db DBUSER DBPASSWORD
echo "Finished adding the Neurobagel vocabulary to the database."

echo "Finished setting up the Neurobagel graph backend."

# We don't have jobcontrol here, so can't bring GraphDB back to foreground
# instead we'll wait
wait $GRAPHDB_PID
