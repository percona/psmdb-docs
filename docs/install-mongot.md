# Install mongot

Before deploying vector search for PSMDB, ensure that you have:

- Percona Server for MongoDB 8.3 or later installed.
- A running standalone, replica set, or sharded deployment.
- Administrative privileges to install and configure `mongot`.
- A supported **Linux operating system**.

For more details, refer to the [vector search compatibility](vector-search-compatibility.md) section.

## Procedure

=== "Tarballs"

    ### Install mongot from tarballs

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

    Configure the following `mongod` parameters to route Search and MongoDB Vector Search queries and manage indexes.

    |**Parameter**|**Description**|
    |--------------|---------------|
    |`searchIndexManagementHostAndPort`|Specifies the host and port of the `mongot` service used for search index management operations.|
    |`mongotHost`|Specifies the host and port of the mongot service used to process search queries. This value must match `searchIndexManagementHostAndPort`.|
            |`skipAuthenticationToSearchIndexManagementServer`|Specifies the host and port of the `mongot` service used for search index management operations.|
    |`useGrpcForSearch`|Enables or disables gRPC communication between `mongod` and `mongot` for MongoDB Search operations.|

    ??? example "Example: mongod config"
        ```sh
        setParameter:
           searchIndexManagementHostAndPort: localhost:27028
           mongotHost: localhost:27028
           skipAuthenticationToSearchIndexManagementServer: false
          useGrpcForSearch: true
        ``` 

    4. Create a user for the `mongot` process on your PSMDB deployment.

    `mongot` must be able to connect to your PSMDB deployment through a user with the `searchCoordinator` role.

        a. Connect to `mongosh` as the admin user.

            ```sh
            mongosh --port 27017 -u <your_admin_username> -p <your_admin_password>
            ```

        b. Connect to the admin database.

            Run the following command to connect to the admin database:

            ```sh
            use admin
            ```

        c. Create your `mongot` user.

                To create a user with the searchCoordinator role:

                - Replace <mongot-username> with a username for your mongot user

                - Replace <mongot-password> with the password that you specify in your passwordFile in the next step

                - Run the following command:

                    ```sh
                    db.createUser(
                        {
                            user: <mongot-username>,
                            pwd: <mongot-password>,
                            roles: [ "searchCoordinator"]
                        }
                    )

    5. Prepare `mongot` directories

        ```sh
        mkdir -p /var/lib/mongot /etc/mongot /opt/mongot
chown mongod: /var/lib/mongot /etc/mongot /opt/mongot
chmod 750 /etc/mongot
        ```

    4.  Create the `mongot` configuration file:

        The tarball contains the following sample configuration file, `config.default.yml`, with the default `mongot` settings. You can modify the settings for your deployment:

        ??? example "Config file"

        ```yaml
        tee /etc/mongot/config.yml <<EOF
        syncSource:
            replicaSet:
              hostAndPort: 127.0.0.1:27017
              username: searchCoordinator
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
            address: "localhost:9946"
        healthCheck:
            address: "localhost:8080"
        logging:
            verbosity: INFO
        EOF
        ```

        !!! note
            The `dataPath` directory in your configuration file must be writable by the user that runs `mongot`.

    5. Create `passwordFile` for `mongot` to connect to `mongod`:

        ```sh
        echo "<mongot-password>" > /etc/mongot/mongot.passwd
        chmod 600 /etc/mongot/mongot.passwd
        chown mongod: /etc/mongot/mongot.passwd
        ```

    6. Copy `mongot` to the installation directory:

        ```sh
        cp -a mongot-community/* /opt/mongot/
        chown -R mongod: /opt/mongot
        ```

    7. Create `systemd` unit file for `mongot`:

        ```sh
        tee /etc/systemd/system/mongot.service <<EOF
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
        EOF
        ```
    8. Adjust the permissions and SELinux security labels (contexts):

    ```sh
    chmod 600 /etc/mongot/config.yml
    restorecon -Rv /opt/mongot
    ```

    9. Enable and start `mongot`:

        ```sh
        sudo systemctl daemon-reload
        sudo systemctl enable mongot
        sudo systemctl start mongot
        ```

    10. Check `mongot` health:

        ```sh
        curl localhost:8080/health
        {"status":"SERVING"}
        ```


















