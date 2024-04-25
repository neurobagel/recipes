# recipes
Configuration files for a Neurobagel deployment.

## How to use
For detailed instructions on the deployment options for Neurobagel, see the official Neurobagel documentation on [setting up a local knowledge graph (node)](https://neurobagel.org/infrastructure/) and [local query federation](https://neurobagel.org/federate/).

### Using the full-stack Docker Compose file

1. Clone the repository
    ```bash
    git clone https://github.com/neurobagel/recipes.git
    ```

2. Copy and rename the required template configuration files
    ```bash
    cp template.env .env

    # if also setting up local federation
    cp local_nb_nodes.template.json local_nb_nodes.json
    ```

    Ensure to edit the configuration file(s) according to your deployment.

    :warning: **Note**: You **must** change the value of the `NB_API_QUERY_URL` variable in the `.env` file before you can launch any service stack that includes a query tool (i.e., `local_node_query`, `full_stack`, `local_federation`). 
See comments in the `.env` file for more information.

3. In the repository root, start the Docker Compose stack and specify your desired deployment profile

    **To set up only a local node:**
    ```bash
    docker compose up -d
    ```
    or
    ```bash
    docker compose --profile local_node up -d
    ```

    **To set up a local node with a graphical query tool:**
    ```bash
    docker compose --profile local_node_query up -d
    ```

    **To set up a local node and local federation (including a graphical query tool) all at once:**
    ```bash
    docker compose --profile full_stack up -d
    ```

    **To set up federation only:**
    
    You may want to do this if you already have local or remote node(s) set up that you now want to send federated queries to.
    ```bash
    docker compose --profile local_federation up -d
    ```

A log file `DEPLOY.log` will be automatically created under `scripts/logs/` with a copy of the STDOUT from the automatic deployment process.
