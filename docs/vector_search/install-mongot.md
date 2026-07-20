# Install mongot

Before deploying Vector Search for Percona Server for MongoDB, ensure that you have:

- Percona Server for MongoDB 8.3 or later installed.
- Administrative privileges to install and configure `mongot`.
- A supported Linux operating system.

Additional requirements depend on the installation method:

- **Tarballs** - An initiated replica set with keyfile access control or sharded deployment. `mongosh` installed on the host.

- **Docker** - Docker engine with Compose v2 installed on the host.

For more information, see [Vector Search compatibility](vector-search-compatibility.md).

## Procedure

=== "Tarballs"

    ### Install `mongot` from tarballs

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

        The extracted archive contains the `mongot` binary, the sample configuration file, the `mongot` launcher script, and the MongoDB Search and Vector Search license files.

    3. Configure `mongod` to communicate with `mongot`.

        Configure the following `mongod` startup parameters.

        | Parameter | Description |
        |-----------|-------------|
        | `searchIndexManagementHostAndPort` | Specifies the host and port of the `mongot` service used for search index management operations. |
        | `mongotHost` | Specifies the host and port of the `mongot` service used to process search queries. This value must match `searchIndexManagementHostAndPort`. |
        | `skipAuthenticationToSearchIndexManagementServer` | Enables or disables authentication between `mongod` and `mongot` for search index management operations. |
        | `useGrpcForSearch` | Enables or disables gRPC communication between `mongod` and `mongot`. |

        ??? example "Example: `mongod` configuration"

            ```yaml
            setParameter:
              searchIndexManagementHostAndPort: localhost:27028
              mongotHost: localhost:27028
              skipAuthenticationToSearchIndexManagementServer: false
              useGrpcForSearch: true
            ```

        These are startup parameters. Restart `mongod` for the changes to take effect.

        ```sh
        sudo systemctl restart mongod
        ```

    4. Create a user for the `mongot` process.

        `mongot` connects to your Percona Server for MongoDB deployment by using a user with the `searchCoordinator` role.

        1. Connect to `mongosh` as an administrator.

            ```sh
            mongosh --port 27017 -u <admin-username> -p <admin-password>
            ```

        2. Switch to the `admin` database.

            ```javascript
            use admin
            ```

        3. Create the `mongot` user.

            Replace:

            - `<mongot-username>` with the username for the `mongot` user.
            - `<mongot-password>` with the password that you save in the password file in the next step.

            Then run:

            ```javascript
            db.createUser({
              user: "<mongot-username>",
              pwd: "<mongot-password>",
              roles: ["searchCoordinator"]
            })
            ```
    5. Create the password file.

        ```sh
        sudo mkdir -p /etc/mongot
        echo -n "<mongot-password>" | sudo tee /etc/mongot/mongot.passwd > /dev/null
        sudo chmod 600 /etc/mongot/mongot.passwd
        sudo chown mongod:mongod /etc/mongot/mongot.passwd
        ```

    6. Prepare the required directories.

        ```sh
        sudo mkdir -p /var/lib/mongot /etc/mongot /opt/mongot
        sudo chown -R mongod:mongod /var/lib/mongot /etc/mongot /opt/mongot
        sudo chmod 750 /etc/mongot
        ```

    7. Create the `mongot` configuration file.

        The tarball includes a sample configuration file named `config.default.yml`. Modify it as needed for your deployment.

        ??? example "Example: `config.default.yml`"

            ```yaml
            syncSource:
              replicaSet:
                hostAndPort: localhost:27017
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

            The user running `mongot` must have write access to the directory specified by `storage.dataPath`.

        For the complete list of configuration options, see the upstream [mongot configuration options :octicons-link-external-16:](https://www.mongodb.com/docs/manual/reference/configuration-options/#std-label-mongot-configuration-options){:target="_blank"} documentation.

    8. Copy the extracted files to the installation directory.

        ```sh
        sudo cp -a mongot-community/* /opt/mongot/
        sudo chown -R mongod:mongod /opt/mongot
        ```

    9. Create the `systemd` service.

        Create the following file:

        ```text
        /etc/systemd/system/mongot.service
        ```

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

    Follow these steps to install and configure `mongot` using Docker:
    {.power-number}

    1. Pull the `mongod` Docker image.

        ```bash
        docker pull percona/percona-server-mongodb:<TAG>
        ```

    2. Pull the `mongot` Docker image.

        ```bash
        docker pull percona/percona-server-mongodb-mongot:<TAG>
        ```

    3. Verify the downloaded images.

        ```bash
        docker image ls | grep percona-server-mongodb
        ```

    4. Create a Docker network.

        The `mongod` and `mongot` containers must run on the same Docker network so that they can communicate using their container names. Use the same `<network-name>` value when you start both containers.

        ```bash
        docker network create <network-name>
        ```
        Replace `<network-name>` with a name for the network, for example `psmdb-search`.

    5. Create the password file for the `mongot` user.

        `mongot` reads the password for its database user from a file. Create the file and restrict its permissions. The `-n` option prevents a trailing newline from being written to the file, which would otherwise become part of the password:


        ```bash
        echo -n "<mongot-password>" > mongot-password.txt
        chmod 400 mongot-password.txt
        ```

        Replace `<mongot-password>` with a password of your choice. You use the same password when you create the `mongot` database user in step 9.

    6. Create the `mongod` configuration file.

        Save the following configuration as `mongod.conf`.

        ```yaml
        net:
          port: 27017
          bindIpAll: true

        replication:
          replSetName: rs0

        setParameter:
          searchIndexManagementHostAndPort: mongot:27028
          mongotHost: mongot:27028
          skipAuthenticationToSearchIndexManagementServer: false
          useGrpcForSearch: true
          searchTLSMode: disabled
        ```

        The `mongot:27028` address consists of the Docker container name and the gRPC port exposed by the `mongot` container. Specify the same value for both `searchIndexManagementHostAndPort` and `mongotHost`.

    7. Start `mongod`.

        Replace:

        - `<path-to-data-db>` with the path to the MongoDB data directory.
        - `<path-to-mongod-conf>` with the path to the `mongod.conf` file.
        - `<network-name>` with the Docker network created in step 4.

        ```bash
        docker run --rm \
          --name mongod \
          -v <path-to-mongod-conf>:/etc/mongod.conf:ro \
          -v <path-to-data-db>:/data/db \
          -p 27017:27017 \
          --network <network-name> \
          percona/percona-server-mongodb:<TAG> \
          --config /etc/mongod.conf
        ```

        The container name `mongod` becomes the hostname used by `mongot` to connect to the database. If you change the container name, update the `syncSource.replicaSet.hostAndPort` value in the `mongot` configuration file.

        To view the server logs:

        ```bash
        docker logs -f mongod
        ```

    8. Initiate the replica set.

        Connect to the running container:

        ```bash
        docker exec -it mongod mongosh --port 27017
        ```

        Initialize the replica set:

        ```javascript
        rs.initiate()
        ```

        Wait until the node becomes the primary replica set member before continuing.

    9. Create the `mongot` user.

        `mongot` requires a database user with the `searchCoordinator` role.

        The `searchCoordinator` role grants `readAnyDatabase` privileges and write access to the internal `__mdb_internal_search` database, which `mongot` uses to store search index metadata.

        1. Switch to the `admin` database.

            ```javascript
            use admin
            ```

        2. Create the user.

            Replace:

            - `<mongot-username>` with the username for the `mongot` user.
            - `<mongot-password>` with the password stored in `mongot-password.txt`.

            ```javascript
            db.createUser({
              user: "<mongot-username>",
              pwd: "<mongot-password>",
              roles: ["searchCoordinator"]
            })
            ```

    10. Create the `mongot` configuration file.

        !!! info "Important"
            Set `syncSource.replicaSet.scramAuth.username` to the user created in the previous step, and `syncSource.replicaSet.scramAuth.passwordFile` to the password file created in step 5.

        For more information about the available configuration options, see the upstream documentation for [mongot configuration options :octicons-link-external-16:](https://www.mongodb.com/docs/manual/reference/configuration-options/#std-label-mongot-configuration-options){:target="_blank"}.

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

        Save the configuration file as `mongot.conf`.

        The `mongod` and `mongot` containers must run on the same Docker network.

        Ensure that:

        - `scramAuth.username` matches the user created in step 9.
        - `passwordFile` points to the password file created in step 5.

        The `mongot` container reads its configuration from `/mongot-community/config.default.yml`, which is mounted in the next step.

    11. Start the `mongot` container.

        Replace:

        - `<path-to-data-mongot>` with the directory used to store search index data.
        - `<path-to-mongot-conf>` with the path to the `mongot.conf` file.
        - `<path-to-password-file>` with the path to the password file.
        - `<network-name>` with the Docker network created in step 4.

        ```bash
        docker run --rm \
          --name mongot \
          -v <path-to-data-mongot>:/data/mongot \
          -v <path-to-mongot-conf>:/mongot-community/config.default.yml:ro \
          -v <path-to-password-file>:/passwordFile:ro \
          --network <network-name> \
          percona/percona-server-mongodb-mongot:<TAG>
        ```

        To view the `mongot` logs:

        ```bash
        docker logs -f mongot
        ```

    12. Verify the health of the `mongot` process.

        Send a request to the readiness endpoint.

        ```bash
        docker exec mongot -- curl localhost:8080/health
        ```

        If `mongot` starts successfully, the endpoint returns:

        ```text
        SERVING
        ```
















    











