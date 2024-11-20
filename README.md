<div align="center">

# recipes
Configuration files for a Neurobagel deployment.

<a href="https://github.com/neurobagel/recipes/actions/workflows/compatibility.yaml">
        <img src="https://img.shields.io/github/actions/workflow/status/neurobagel/query-tool/component-test.yaml?color=8FBC8F&label=Tool version compatibility test&style=flat-square" alt="Tool version compatibility test">
    </a>
</div>

## How to use
For detailed instructions on deploying Neurobagel for your use case, see the official Neurobagel documentation on [setting up a local knowledge graph (node)](https://neurobagel.org/user_guide/getting_started/) and [configuration options](https://neurobagel.org/user_guide/config/).

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

    Ensure to edit the [configuration file(s)](https://neurobagel.org/user_guide/config/) according to your deployment.
    **We strongly recommend changing the default passwords for your GraphDB instance, which are set using `NB_GRAPH_ADMIN_PASSWORD.txt` and `NB_GRAPH_PASSWORD.txt` in the ./secrets subdirectory by default.**

    :warning: **Note**: You **must** change the value of the `NB_API_QUERY_URL` variable in the `.env` file before you can launch any service stack that includes a query tool (i.e., `full_stack`, `local_federation`). 
See comments in the `.env` file for more information.

3. In the repository root, start the Docker Compose stack and specify your desired deployment profile

    **To set up a local node along with a graphical query tool and optional federation:**
    ```bash
    docker compose up -d
    ```
    or
    ```bash
    docker compose --profile full_stack up -d
    ```

    **To set up only a local node (without a graphical query tool):**
    ```bash
    docker compose --profile local_node up -d
    ```

    **To set up federation only:**
    
    You may want to do this if you already have local or remote node(s) set up that you now want to send federated queries to.
    ```bash
    docker compose --profile local_federation up -d
    ```

A log file `DEPLOY.log` will be automatically created under `scripts/logs/` with a copy of the STDOUT from the automatic deployment process.
