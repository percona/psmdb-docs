# Install mongot

Before deploying Vector Search for Percona Server for MongoDB, ensure that you have:

- Percona Server for MongoDB 8.3 or later installed.
- An initiated replica set with keyfile access control or sharded deployment.
- Administrative privileges to install and configure `mongot`.
- A supported Linux operating system.
- Docker engine with Compose v2 (if you are installing on Docker).
- `mongosh` installed on the host.

For more information, see [Vector Search compatibility](vector-search-compatibility.md).

## Procedure

=== "Tarballs"

    ### Install mongot from tarballs

    Follow these steps to install `mongot` from a tarball:
    {.power-number}

    1. Download the `mongot` tarball.

        === "ARM64"

            Download the [ARM64 tarball :octicons-link-external-16:](https://downloads.mongodb.org/mongodb-search-community/0.53.0/mongot_community_0.53.0_linux_aarch64.tgz){:target="_blank"}.

        === "AMD64 (x86_64)"

            Download the [AMD64 tarball :octicons-link-external-16:](https://downloads.mongodb.org/mongodb-search-community/0.53.0/mongot_community_0.53.0_linux_x86_64.tgz){:target="_blank"}.

    2. Extract the tarball.

        === "ARM64"

            ```sh
            tar -zxvf mongot_community_0.53.0_linux_aarch64.tgz
            ```

        === "AMD64 (x86_64)"

            ```sh
            tar -zxvf mongot_community_0.53.0_linux_x86_64.tgz
            ```

        The extracted archive contains the `mongot` binary, a sample configuration file, the `mongot` launcher script, and MongoDB Search and Vector Search license information.

    3. Configure `mongod` to communicate with `mongot`.

        Configure the following `mongod` parameters.

        | Parameter | Description |
        |-----------|-------------|
        | `searchIndexManagementHostAndPort` | Specifies the host and port of the `mongot` service used for search index management operations. |
        | `mongotHost` | Specifies the host and port of the `mongot` service used to process search queries. This value must match `searchIndexManagementHostAndPort`. |
        | `skipAuthenticationToSearchIndexManagementServer` | Enables or disables authentication between `mongod` and `mongot` for search index management operations. |
        | `useGrpcForSearch` | Enables or disables gRPC communication between `mongod` and `mongot`. |

        ??? example "Example: mongod configuration"

            ```yaml
            setParameter:
              searchIndexManagementHostAndPort: localhost:27028
              mongotHost: localhost:27028
              skipAuthenticationToSearchIndexManagementServer: false
              useGrpcForSearch: true
            ```

    4. Create a user for the `mongot` process.

        `mongot` must be able to connect to your Percona Server for MongoDB deployment through a user with the `searchCoordinator` role.

        a. Connect to `mongosh` as an administrator.

            ```sh
            mongosh --port 27017 -u <admin-username> -p <admin-password>
            ```

        b. Switch to the `admin` database.

            ```javascript
            use admin
            ```

        c. Create the `mongot` user.

        Replace:

        - `<mongot-username>` with the username for the `mongot` user.
        - `<mongot-password>` with the password that you will save in the password file in the next step.

        Then run:

        ```javascript
        db.createUser({
          user: "<mongot-username>",
          pwd: "<mongot-password>",
          roles: ["searchCoordinator"]
        })
        ```

    5. Prepare the required directories.

        ```sh
        sudo mkdir -p /var/lib/mongot /etc/mongot /opt/mongot
        sudo chown -R mongod:mongod /var/lib/mongot /etc/mongot /opt/mongot
        sudo chmod 750 /etc/mongot
        ```

    6. Create the `mongot` configuration file.

        The tarball includes a sample configuration file, `config.default.yml`. Modify it as needed for your deployment.

        ??? example "Example: Configuration file"

            ```yaml
            syncSource:
              replicaSet:
                hostAndPort: 127.0.0.1:27017
                username: <mongot-username>
                passwordFile: /etc/mongot/mongot.passwd
                tls: false

            storage:
              dataPath: /var/lib/mongot

            server:
              grpc:
                address: localhost:27028
                tls:
                  mode: disabled

            metrics:
              enabled: true
              address: localhost:9946

            healthCheck:
              address: localhost:8080

            logging:
              verbosity: INFO
            ```

        !!! note

            Ensure that the directory specified by `storage.dataPath` is writable by the user running `mongot`.

    7. Create the password file.

        ```sh
        echo "<mongot-password>" | sudo tee /etc/mongot/mongot.passwd > /dev/null
        sudo chmod 600 /etc/mongot/mongot.passwd
        sudo chown mongod:mongod /etc/mongot/mongot.passwd
        ```

    8. Copy the extracted files to the installation directory.

        ```sh
        sudo cp -a mongot-community/* /opt/mongot/
        sudo chown -R mongod:mongod /opt/mongot
        ```

    9. Create the `systemd` service.

        ```ini
        [Unit]
        Description=MongoDB Search (mongot)
        Documentation=https://www.mongodb.com/docs/manual/reference/configuration-options/#std-label-mongot-configuration-options
        After=network.target

        [Service]
        User=mongod
        Group=mongod
        Type=simple
        ExecStart=/opt/mongot/mongot --config /etc/mongot/config.yml
        Restart=on-failure
        RestartSec=5
        LimitNOFILE=64000
        TimeoutStartSec=30
        TimeoutStopSec=30
        SuccessExitStatus=143

        [Install]
        WantedBy=multi-user.target
        ```

        Save the file as:

        ```text
        /etc/systemd/system/mongot.service
        ```

    10. Set the required file permissions and SELinux contexts.

        ```sh
        sudo chown mongod:mongod /etc/mongot/config.yml
        sudo chmod 600 /etc/mongot/config.yml
        sudo restorecon -Rv /opt/mongot
        ```

    11. Enable and start `mongot`.

        ```sh
        sudo systemctl daemon-reload
        sudo systemctl enable mongot
        sudo systemctl start mongot
        ```

    12. Verify that `mongot` is running.

        ```sh
        curl localhost:8080/health
        ```

        Example output:

        ```json
        {"status":"SERVING"}
        ```

=== "Docker"

    ### Install Vector Search with Docker

    !!! info "Important"
        - `mongot` synchronizes data from `mongod` and requires a PSMDB replica set. Standalone deployments are not supported.
        - If you want PSMDB Vector Search to automatically generate embeddings for text stored in your collections, create endpoint service API keys. For more information, see **Automated Embedding**.

    Follow these steps to install and configure `mongot` using Docker:
    {.power-number}

    1. Pull the `mongod` Docker image.

        ```bash
        docker pull percona/percona-server-mongodb:<tag>
        ```

    2. Pull the `mongot` Docker image.

        ```bash
        docker pull percona/percona-server-mongodb-mongot:<tag>
        ```

    3. Verify the downloaded images.

        ```bash
        docker image ls | grep percona-server-mongodb
        ```

    4. Create a Docker network.

        Create a Docker network for communication between the `mongod` and `mongot` containers.

        ```bash
        docker network create <docker-network-name>
        ```

    5. Create the `mongod` configuration file.

        Save the following configuration as `mongod.conf`.

        ```yaml
        net:
          port: 27017
          bindIpAll: true

        replication:
          replSetName: rs0

        setParameter:
          searchIndexManagementHostAndPort: <mongot-container-name>:27028
          mongotHost: <mongot-container-name>:27028
          skipAuthenticationToSearchIndexManagementServer: false
          useGrpcForSearch: true
          searchTLSMode: disabled
        ```

    6. Start `mongod`.

        Replace:

        - `<path-to-data-db>` with the path to the MongoDB data directory.
        - `<path-to-mongod-conf>` with the path to the `mongod.conf` file.
        - `<docker-network-name>` with the Docker network created in the previous step.

        ```bash
        docker run --rm \
          --name mongod \
          -v <path-to-mongod-conf>:/etc/mongod.conf:ro \
          -v <path-to-data-db>:/data/db \
          -p 27017:27017 \
          --network <docker-network-name> \
          percona/percona-server-mongodb:8.3.4-1 \
          --config /etc/mongod.conf \
          --replSet rs0
        ```

    7. Connect to the database.

        Open a new terminal and connect to the running `mongod` instance.

        ```bash
        docker exec -it mongod mongosh --port 27017
        ```

    8. Create a user for the `mongot` process.

        `mongot` requires a database user with the `searchCoordinator` role.

        The `searchCoordinator` role grants `readAnyDatabase` privileges and write access to the internal `__mdb_internal_search` database, which `mongot` uses to store search index metadata.

        a. Switch to the `admin` database.

        ```javascript
        use admin
        ```

        b. Create the `mongot` user.

        Replace:

        - `<mongot-username>` with the username for the `mongot` user.
        - `<mongot-password>` with the password that you will store in the password file.

        ```javascript
        db.createUser({
          user: "<mongot-username>",
          pwd: "<mongot-password>",
          roles: ["searchCoordinator"]
        })
        ```

    9. Create the `mongot` configuration file.

        !!! info "Important"
            Set `syncSource.replicaSet.scramAuth.username` to the user created in the previous step, and set `syncSource.replicaSet.scramAuth.passwordFile` to the password file that contains that user's password.

        For more information about the available configuration options, see the MongoDB documentation for [mongot configuration options :octicons-link-external-16:](https://www.mongodb.com/docs/manual/reference/configuration-options/#std-label-mongot-configuration-options){:target="_blank"}.

        ??? example "Example: `mongot.conf`"

            ```yaml
            syncSource:
              replicaSet:
                hostAndPort: "mongod:27017"
                scramAuth:
                  username: "mongotUser"
                  passwordFile: "/passwordFile"
                  authSource: "admin"
                  tls:
                    enabled: false
              replicationReader:
                readPreference: "secondaryPreferred"

            storage:
              dataPath: "/data/mongot"

            server:
              grpc:
                address: "mongot:27028"
                tls:
                  mode: "disabled"

            metrics:
              enabled: true
              address: "mongot:9946"

            healthCheck:
              address: "mongot:8080"

            logging:
              verbosity: INFO
            ```

        Save the configuration as `mongot.conf` or another preferred file name.

        Both the `mongod` and `mongot` containers must run on the same Docker network.

    10. Start the `mongot` container.

        Replace:

        - `<path-to-data-mongot>` with the directory used to store search index data.
        - `<path-to-mongot-conf>` with the path to the `mongot.conf` file.
        - `<path-to-password-file>` with the path to the password file.
        - `<docker-network-name>` with the Docker network created earlier.

        ```bash
        docker run --rm \
          --name mongot \
          -v <path-to-data-mongot>:/data/mongot \
          -v <path-to-mongot-conf>:/mongot-community/config.default.yml:ro \
          -v <path-to-password-file>:/passwordFile:ro \
          --network <docker-network-name> \
          -p 27028:27028 \
          -p 8080:8080 \
          -p 9946:9946 \
          percona/percona-server-mongodb-mongot:1.70.1-1
        ```

    11. Verify the health of the `mongot` process.

        Send a request to the readiness endpoint.

        ```bash
        curl localhost:8080/health
        ```

        If `mongot` is running successfully, the endpoint returns:

        ```text
        SERVING
        ```
















    











