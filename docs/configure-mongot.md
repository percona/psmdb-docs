# Configure mongot

After installing `mongot`, configure it to connect to the Percona Server for MongoDB replica set, store search indexes, and accept search requests from `mongod`.

Vector Search requires configuration on both sides:

- `mongot` must be able to connect to the replica set and synchronize data.
- `mongod` must know where to send search queries and search-index management requests.

!!! note
    The examples in this section use a single-node test environment with `mongod` listening on port **27017** and `mongot` listening on port **27028**. Replace the host names, ports, paths, and credentials with values that are applicable for your deployment.

## Before you begin

- PSMDB is running as an initialized replica set.
- Authentication is enabled.
- The `mongot` binary is installed.
- The user running `mongot` can write to the search data and log directories.
- The host running `mongot` can connect to the replica set.
- The required ports are available.

## Procedure







