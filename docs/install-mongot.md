# Install mongot

Before deploying vector search for PSMDB, ensure that you have:

- Percona Server for MongoDB 8.3 or later installed.
- A running standalone, replica set, or sharded deployment.
- Administrative privileges to install and configure `mongot`.
- A supported **Linux operating system**.

For more details, refer to the [vector search compatibility](vector-search-compatibility.md) section.

## Procedure

### Install from binary tarball

Follow these steps to install `mongot` from tarball:
{.power-number}

1. Download the `mongot` tarball. 

    Click the following link to download the Search in tarball.

    === "ARM Architectures"

        For `ARM architectures`, use [ARM-compatible tarball :octicons-link-external-16:](https://downloads.mongodb.org/mongodb-search-community/0.53.0/mongot_community_0.53.0_linux_aarch64.tgz){:target="_blank"}.

    === "AMD x86_64 Architectures"

        For `AMD x86_64` architectures, use [AMD x86-64-compatible tarball :octicons-link-external-16:](https://downloads.mongodb.org/mongodb-search-community/0.53.0/mongot_community_0.53.0_linux_x86_64.tgz){:target="_blank"}.


2. Extract the `mongot` tarball.

    Run the following command to extract the tarball:

    === "ARM Architectures"

        ```sh
        tar -zxvf mongot_community_0.53.0_linux_aarch64.tgz
        ```

    === "AMD x86_64 Architectures"

        ```sh
        tar -zxvf mongot_community_0.53.0_linux_aarch64.tgz
        ```

    The tarball contains a sample configuration file, the `mongot` launcher script, and MongoDB Search and Vector Search license information.

3. Configure `mongod` to communicate with `mongot`.

    If you have an existing replica set that you want to use, configure the following `mongod` parameters to route Search and MongoDB Vector Search queries and manage indexes.







