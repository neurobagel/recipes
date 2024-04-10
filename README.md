# recipes
Configuration files for a Neurobagel deployment.

## How to use
For detailed instructions on the deployment options for Neurobagel, see the official Neurobagel documentation on [setting up a local knowledge graph (node)](https://neurobagel.org/infrastructure/) and [local query federation](https://neurobagel.org/federate/).

### Using the full-stack Docker Compose file

1. Clone the repository
```bash
git clone https://github.com/neurobagel/recipes.git
```

2. `cd` into the directory containing the Neurobagel deployment recipe
<!---
TODO: Change once we rename this directory for production!
-->
```bash
cd recipes/dev
```

3. Copy and rename template files in the directory
```bash
cp template.env .env

# if also setting up local federation
cp local_nb_nodes.template.json local_nb_nodes.json
```
Ensure to edit the file(s) according to your deployment.

4. Start the Docker Compose stack and specify your desired deployment profile

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

    **To set up a local node and local federation (including a graphical query tool):**
    ```bash
    docker compose --profile full_stack up -d
    ```
A log file `DEPLOY.log` will be automatically created in the current directory with a copy of the STDOUT from the automatic deployment process.

### Using deployment type-specific Docker Compose files

**Note: These instructions will soon be superceded by the full-stack Docker Compose file instructions.**

1. Clone the repository
```bash
git clone https://github.com/neurobagel/recipes.git
```

2. `cd` into the directory containing the appropriate configuration files
for your deployment scenario.

3. Depending on your deployment scenario, 
copy and/or rename the template files in the directory
and edit them accordingly:
    
    `local_federation/`
    - `local_nb_nodes.json`
    - `.env`

    `local_node/`
    - `.env`
    
    `local_node_with_query_tool/`
    - `.env`
