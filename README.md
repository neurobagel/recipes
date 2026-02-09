<div align="center">

# recipes

Configuration files for a Neurobagel deployment.

<a href="https://github.com/neurobagel/recipes/actions/workflows/compatibility.yaml">
        <img src="https://img.shields.io/github/actions/workflow/status/neurobagel/query-tool/component-test.yaml?color=8FBC8F&label=Tool version compatibility test&style=flat-square" alt="Tool version compatibility test">
    </a>
</div>

## How to use

For detailed instructions on deploying Neurobagel for your use case, see the official Neurobagel documentation on [setting up a local knowledge graph (node)](https://neurobagel.org/user_guide/getting_started/) and [configuration options](https://neurobagel.org/user_guide/config/).

### Deploying locally for testing

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

    Edit the [configuration file(s)](https://neurobagel.org/user_guide/config/) according to your deployment.
    **We strongly recommend changing the default passwords for your GraphDB instance, which are set using `NB_GRAPH_ADMIN_PASSWORD.txt` and `NB_GRAPH_PASSWORD.txt` in the ./secrets subdirectory by default.**

See comments in the `.env` file for more information.

1. In the repository root, start the default Docker Compose recipe

    ```bash
    docker compose up -d
    ```

A log file `DEPLOY.log` will be automatically created under `scripts/logs/` with a copy of the STDOUT from the automatic deployment process.
