#!/bin/bash

echo "The script is running..."

/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=/opt/graphdb/ &

# Waiting for GraphDB to start
while ! curl --silent "localhost:7200/rest/repositories" | grep '\[\]'; do
    :
done

echo "Running GraphDB setup..."

./graphdb_setup.sh apple

echo "GraphDB set up complete."

echo "Adding data to databases..."
./add_data_to_graph.sh ./data localhost:7200 repositories/my_db DBUSER DBPASSWORD


tail -f /dev/null

