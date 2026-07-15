# Install mongot

Before deploying Vector Search for Percona Server for MongoDB, ensure that you have:

- Percona Server for MongoDB 8.3 or later installed.
- A running standalone, replica set, or sharded deployment.
- Administrative privileges to install and configure `mongot`.
- A supported Linux operating system.

For more information, see [Vector Search compatibility](vector-search-compatibility.md).

## Procedure

=== "Tarballs"

    ### Install mongot from tarballs:

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

        ??? example "Example configuration"

            ```yaml
            syncSource:
              replicaSet:
                hostAndPort: 127.0.0.1:27017
                username: "<mongot-username>"
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
        read -s -p "Enter mongot password: " MONGOT_PASSWORD && echo
        printf "%s" "$MONGOT_PASSWORD" | sudo tee /etc/mongot/mongot.passwd > /dev/null
        unset MONGOT_PASSWORD
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