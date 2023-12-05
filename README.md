# recipes
Configuration files for a Neurobagel deployment.

## How to use
For detailed instructions on the deployment options for Neurobagel, see the official Neurobagel documentation on [setting up a local knowledge graph (node)](https://neurobagel.org/infrastructure/) and [local query federation](https://neurobagel.org/federate/).

1. Clone the repository
```bash
git clone https://github.com/neurobagel/recipes.git
```

2. `cd` into the directory containing the relative configuration files for your deployment.

3. Depending on your deployment, create the following parameters file(s) following the template(s) provided in that directory:
    
    `local_federation/`
    - `local_nb_nodes.json`
    - `.env`

    `local_node/`
    - `.env`
    
    `local_node_with_query_tool/`
    - `.env`
