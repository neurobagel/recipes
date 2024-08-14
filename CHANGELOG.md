# v0.1.0 (Wed Aug 14 2024)

#### 💥 Breaking Changes

- [MNT] Renamed `NB_QUERY_URL_PATH` env var to `NB_QUERY_APP_BASE_PATH` [#77](https://github.com/neurobagel/recipes/pull/77) ([@rmanaem](https://github.com/rmanaem))
- [ENH] Removed `local_node_query` profile [#72](https://github.com/neurobagel/recipes/pull/72) ([@rmanaem](https://github.com/rmanaem))

#### 🚀 Enhancements

- [FIX] Revert default image tags to `latest` [#79](https://github.com/neurobagel/recipes/pull/79) ([@alyssadai](https://github.com/alyssadai))

#### 🏠 Internal

- [MNT] Updated `compatibility.yaml` file and e2e tests [#78](https://github.com/neurobagel/recipes/pull/78) ([@rmanaem](https://github.com/rmanaem))

#### Authors: 2

- Alyssa Dai ([@alyssadai](https://github.com/alyssadai))
- Arman Jahanpour ([@rmanaem](https://github.com/rmanaem))

---

# v0.0.1 (Wed Aug 07 2024)

:tada: This release contains work from new contributors! :tada:

Thanks for all your work!

:heart: Alyssa Dai ([@alyssadai](https://github.com/alyssadai))

:heart: Arman Jahanpour ([@rmanaem](https://github.com/rmanaem))

:heart: Sebastian Urchs ([@surchs](https://github.com/surchs))

### Release Notes

#### [CI] Make first release ([#76](https://github.com/neurobagel/recipes/pull/76))

First release of the Neurobagel deployment recipe. This release introduces different deployment profiles and an automated process for setting up a graph store using Docker Compose, as well as various environment variables for configuring the behaviour of Neurobagel services using a single `.env` file.

<!-- To be checked off by reviewers -->

---

#### 🚀 Enhancements

- [CI] Make first release [#76](https://github.com/neurobagel/recipes/pull/76) ([@alyssadai](https://github.com/alyssadai))
- [ENH] Added `NB_QUERY_APP_BASE_PATH` [#69](https://github.com/neurobagel/recipes/pull/69) ([@alyssadai](https://github.com/alyssadai) [@rmanaem](https://github.com/rmanaem))
- [ENH] add auth vars to n-API & local query tool and disable by default [#67](https://github.com/neurobagel/recipes/pull/67) ([@alyssadai](https://github.com/alyssadai))
- [ENH] Update environment variables and remove deprecated `version` tag [#65](https://github.com/neurobagel/recipes/pull/65) ([@alyssadai](https://github.com/alyssadai))
- [ENH] Added `NB_FEDERATE_REMOTE_PUBLIC_NODES` env var [#61](https://github.com/neurobagel/recipes/pull/61) ([@rmanaem](https://github.com/rmanaem))
- [FIX] Enable graph setup to run on stack restart [#57](https://github.com/neurobagel/recipes/pull/57) ([@surchs](https://github.com/surchs))
- [MNT] Use docker compose secrets for sensitive credentials [#50](https://github.com/neurobagel/recipes/pull/50) ([@alyssadai](https://github.com/alyssadai))
- [ENH] Add `COMPOSE_PROJECT_NAME` to template.env [#48](https://github.com/neurobagel/recipes/pull/48) ([@alyssadai](https://github.com/alyssadai))
- [REF] Consolidate deployment recipes and refactor template.env [#46](https://github.com/neurobagel/recipes/pull/46) ([@alyssadai](https://github.com/alyssadai))
- [ENH] Separate /data mount points, separate query tool profiles [#44](https://github.com/neurobagel/recipes/pull/44) ([@alyssadai](https://github.com/alyssadai))
- [FIX] Remove default `NB_API_QUERY_URL` value and fix ports used by full-stack setup script [#42](https://github.com/neurobagel/recipes/pull/42) ([@alyssadai](https://github.com/alyssadai))
- [FIX] Use `NB_GRAPH_ROOT_CONT` in `setup.sh` [#43](https://github.com/neurobagel/recipes/pull/43) ([@surchs](https://github.com/surchs))
- [ENH] Add single docker compose recipe for all deployment flavours [#32](https://github.com/neurobagel/recipes/pull/32) ([@rmanaem](https://github.com/rmanaem) [@surchs](https://github.com/surchs) [@alyssadai](https://github.com/alyssadai))
- [FIX] Switch query tool port to default used by Vite [#31](https://github.com/neurobagel/recipes/pull/31) ([@alyssadai](https://github.com/alyssadai))
- [REF] Rename `API_QUERY_URL` to `NB_API_QUERY_URL` [#26](https://github.com/neurobagel/recipes/pull/26) ([@alyssadai](https://github.com/alyssadai))
- [FIX] Consolidate `add_data_to_graph.sh` [#23](https://github.com/neurobagel/recipes/pull/23) ([@alyssadai](https://github.com/alyssadai) [@surchs](https://github.com/surchs))
- [ENH] Add GraphDB setup script [#19](https://github.com/neurobagel/recipes/pull/19) ([@alyssadai](https://github.com/alyssadai))
- [FIX] Update environment variable table with GraphDB defaults [#17](https://github.com/neurobagel/recipes/pull/17) ([@alyssadai](https://github.com/alyssadai))
- [REF] Switch to opt-in Stardog syntax [#13](https://github.com/neurobagel/recipes/pull/13) ([@surchs](https://github.com/surchs))
- [REF] Move vocab turtle file from api repo [#15](https://github.com/neurobagel/recipes/pull/15) ([@surchs](https://github.com/surchs) [@alyssadai](https://github.com/alyssadai))
- [FIX] Use `host-gateway` instead of `localhost` in local federation config [#6](https://github.com/neurobagel/recipes/pull/6) ([@alyssadai](https://github.com/alyssadai))
- [ENH] Add configuration files and templates for different deployment flavours [#2](https://github.com/neurobagel/recipes/pull/2) ([@alyssadai](https://github.com/alyssadai))

#### ⚠️ Pushed to `main`

- Initial commit ([@alyssadai](https://github.com/alyssadai))

####  🧪 Tests

- [FIX] Fix the compatibility workflows [#51](https://github.com/neurobagel/recipes/pull/51) ([@surchs](https://github.com/surchs))
- [ENH] Add version compatibility check for all latest builds [#37](https://github.com/neurobagel/recipes/pull/37) ([@surchs](https://github.com/surchs))
- [CI] Set up `compatibility test` workflow [#35](https://github.com/neurobagel/recipes/pull/35) ([@rmanaem](https://github.com/rmanaem))

#### Authors: 3

- Alyssa Dai ([@alyssadai](https://github.com/alyssadai))
- Arman Jahanpour ([@rmanaem](https://github.com/rmanaem))
- Sebastian Urchs ([@surchs](https://github.com/surchs))
